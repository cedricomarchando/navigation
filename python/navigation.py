# %%
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
from matplotlib.path import Path # For marker construction
import nautical_marker as  marker
import pandas as pd
import math


class Waypoint:
    """ create a waypoint object """
    def __init__(self, position :list[float, float], waypoint_number = None):
        self.position = position
        self.waypoint_number = waypoint_number
        
    def plot(self):
        plt.plot(self.position[0], self.position[1], 'o')
        
    def __str__(self):
        return f' x={self.position[0]}, y={self.position[1]}, waypoint_id={self.waypoint_number}\n'


class BoatSimu:
    """ BoatSimu class, 
    instantian Boat_true that represent the boat wit its true parameter
    and boat_estimate taht represent the boat with estimated parameters"""
    def __init__(self, true_position:list[float, float]):
        self.boat_true = Boat( true_position, color='g')
        self.boat_estimate = Boat( true_position, color='r')

    def plot_boat(self) ->None:
        " plot boat true and boat estimate"
        self.boat_true.plot_boat("True boat")
        self.boat_estimate.plot_boat("Estimated boat")

    def compute_position_3lop(self, mark1, mark2, mark3):
        """ Comput fix position with triangulation of 3 Lines Of Position (LOP) """
        sigma = np.pi/90 # 2 degree
        mark1.compute_bearing(self.boat_true,sigma)
        mark2.compute_bearing(self.boat_true,sigma)
        mark3.compute_bearing(self.boat_true,sigma)
        intersection1 = compute_intersection(mark1, mark2)
        intersection2 = compute_intersection(mark2, mark3)
        intersection3 = compute_intersection(mark1, mark3)
        #compute barycentre using Chasles formula
        barycentre = (intersection1 + intersection2 + intersection3)/3
        #circonscribed_circle does not work
        plt.plot( (intersection1[0], intersection2[0], intersection3[0], intersection1[0]),
                (intersection1[1], intersection2[1], intersection3[1], intersection1[1]),'g')
        self.boat_estimate.set_position(barycentre)
        return barycentre

    def compute_position_2lop(self, mark1_up, mark2_up, show_lop):
        """ Compute estimated position with 2 LOP"""
        mark1_down = Mark(mark1_up.position)
        mark2_down = Mark(mark2_up.position)

        sigma = np.pi/90 # 2d egrees
        mark1_up.compute_bearing(self.boat_true,sigma)
        mark2_up.compute_bearing(self.boat_true,sigma)
        mark1_down.compute_bearing(self.boat_true,-sigma)
        mark2_down.compute_bearing(self.boat_true,-sigma)
        if show_lop:
            mark1_up.plot_mark_bearing(self.boat_true)
            mark2_up.plot_mark_bearing(self.boat_true)
            mark1_down.plot_mark_bearing(self.boat_true)
            mark2_down.plot_mark_bearing(self.boat_true)

        inter1 = compute_intersection(mark1_up,mark2_up)
        inter2 = compute_intersection(mark1_up,mark2_down)
        inter3 = compute_intersection(mark1_down,mark2_down)
        inter4 = compute_intersection(mark1_down,mark2_up)

        plt.plot( (inter1[0], inter2[0], inter3[0], inter4[0], inter1[0]),
                (inter1[1], inter2[1], inter3[1], inter4[1],  inter1[1]),'k')
        plt.fill( (inter1[0], inter2[0], inter3[0], inter4[0], inter1[0]),
                (inter1[1], inter2[1], inter3[1], inter4[1],  inter1[1]),'g',label="position area")
        
        barycentre = (inter1 + inter2 + inter3 + inter4)/4
        self.boat_estimate.set_position(barycentre)
        return barycentre
    
    def run_fix(self, mark, duration, sigma):
        """ Run fix: get position from 1 mark and speed """
        mark.compute_bearing(self.boat_true, sigma)
        save_bearing = mark.bearing
        # compute updated bearing after running
        self.boat_true.run(duration)
        mark.compute_bearing(self.boat_true, sigma)
        mark.plot_mark_bearing(self.boat_true)
        # run mark in the direction of the boat
        duration = 1
        mark_tmp = Mark(
            [mark.position[0] + self.boat_estimate.speed * duration * np.sin(self.boat_estimate.course),
            mark.position[1] + self.boat_estimate.speed * duration * np.cos(self.boat_estimate.course)],
            bearing = save_bearing
            )
        plt.plot(mark_tmp.position[0], mark_tmp.position[1],'+k', label ="mark shifted")

        mark_tmp.plot_mark_bearing(self.boat_true)

        estimate = compute_intersection(mark,mark_tmp)
        del mark_tmp
        self.boat_estimate.set_position(estimate)
        return estimate
    
    def update_3lop_fix(self, marks_map, sigma) -> None:
        marks_map.compute_fixed_mark_disance(self.boat_estimate)
        nearest_marks = marks_map.select_near_fixed_marks(6)
        for mark in nearest_marks:
            mark.compute_bearing(self.boat_true, sigma)
        markA, markB, markC = get_best_marks(nearest_marks)
        self.compute_position_3lop(markA, markB, markC)
        self.plot_boat()
        #markA.plot_mark_bearing(self.boat_true)
        #markB.plot_mark_bearing(self.boat_true)
        #markC.plot_mark_bearing(self.boat_true)
    
    def run(self,duration : float):
        self.boat_estimate.run(duration)
        self.boat_true.run(duration)
        
    def set_course(self, position:list[float, float]):
        self.boat_estimate.set_course(position)
        self.boat_true.set_course(position)
        
    def compute_waypoint_distance(self, waypoint:Waypoint) -> None:
        self.boat_estimate.compute_waypoint_distance(waypoint)
        self.boat_true.compute_waypoint_distance(waypoint)
        
    def go_to_waypoint(self, waypoint:Waypoint, marks_map, sigma, fix_period):
        self.compute_waypoint_distance(waypoint)
        while self.boat_true.waypoint_distance > self.boat_true.speed * fix_period:
            self.set_course(waypoint.position)
            self.run(fix_period)
            self.update_3lop_fix(marks_map, sigma)
            self.compute_waypoint_distance(waypoint)


class Boat:
    """ Boat class """
    def __init__(self, position :list[float, float], course = None, speed = None, waypoint_distance = None, color ='b'):
        self.position = position
        self.speed = speed
        self.course = course
        self.color = color
        self.waypoint_distance = waypoint_distance

    def plot_speed(self):
        """ Show speed with direction of course"""
        plt.arrow(self.position[0], self.position[1],
                  self.speed * np.sin(self.course),
                  self.speed * np.cos(self.course),
                  head_width = 10)

    def run(self,duration):
        """ Run with speed for a duration """
        self.position[0] += self.speed * duration * np.sin(self.course)
        self.position[1] += self.speed * duration * np.cos(self.course)

    def plot_position(self):
        """ Plot position """
        plt.plot(self.position[0], self.position[1], '^b', markerfacecolor='none', label='Boat position')

    def plot_boat(self,label = None):
        """ plot with a boat marker in the direction of the course """
        vertices = [(-2, 1), (1, 2), (3, 0), (1, -2), (-2, -1), (-2, 1)]
        codes = [1,3,2,3,1,79]
        boat_marker = Path(vertices,codes)
        if self.course is not None:
            angle = self.course - np.pi/2
            boat_marker = boat_marker.transformed(transforms.Affine2D().rotate(-angle))
        plt.plot(self.position[0], self.position[1], marker=boat_marker,
            markersize=10, color=self.color,  markerfacecolor='none',
            linestyle = 'None', label=label)

    def set_position(self,position : list[float, float]) -> None:
        """ Set boat with new position """
        self.position = position
        
    def set_course(self, position :list[float, float]) -> None:
        """ give course to go to position """
        vector_x = position[0] - self.position[0]
        vector_y = position[1] - self.position[1]
        self.course = np.arctan2(vector_x, vector_y)

    def compute_waypoint_distance(self, waypoint:Waypoint) -> float:
        self.waypoint_distance = math.dist(self.position, waypoint.position)
    
    
class Mark:
    """ Mark class, including landmarks and Seamarks """
    def __init__(self,position :list[float, float], mark_type = 'lighthouse',  top_mark_type = None,
                 light_color = None, name = None, floating:bool=False, show_top_mark=True, bearing = None, distance = None):
        self.position = position
        self.mark_type = mark_type.lower()
        self.top_mark_type = top_mark_type
        self.light_color = light_color
        self.name = name
        self.floating = floating
        self.show_top_mark = show_top_mark
        self.bearing = bearing
        self.distance = distance

    def plot_mark(self):
        """ Plot position"""
        marker.PlotMark( self.position[0], self.position[1], self.mark_type, self.top_mark_type,
                        self.light_color, self.name, self.floating, self.show_top_mark  )

    def plot_mark_bearing(self, boat:Boat):
        """ Plot LOP of a mark with dotted line"""
        x_line = np.linspace(self.position[0],boat.position[0],10)
        y_line = x_line * 1/np.tan(self.bearing) + self.position[1] - self.position[0] *  1/np.tan(self.bearing)
        plt.plot(x_line, y_line, '--k', linewidth=0.5, label = "Line of Position (LoP)")

    def compute_bearing(self, boat:Boat, sigma):
        """ compute Bearing angle of a mark from the point of vie of the Boat """
        vector_x = self.position[0] - boat.position[0]
        vector_y = self.position[1] - boat.position[1]
        bearing = np.arctan2(vector_x, vector_y)
        # bearing = bearing + random.normalvariate(mu=0.0,sigma = sigma)
        self.bearing = bearing + sigma
    
    def compute_distance(self, boat:Boat):
        distance = math.dist(self.position, boat.position)
        self.distance = distance
    
    def __str__(self):
        return (f' x={self.position[0]}, y={self.position[1]}, mark_type={self.mark_type}, top_mark={self.top_mark_type},'
                f'name={self.name}, floating={self.floating}, distance={self.distance}\n')


class MarksMap:
    """ Build map with all marks"""
    def __init__(self):
        self.map_marks = []
        self.fixed_marks = []
    
    def append_mark(self, mark:Mark):
        self.map_marks.append(mark)
        if mark.mark_type in marker.LANDMARKS_SET:
            self.fixed_marks.append(mark)
        if (mark.mark_type in marker.SEAMARK_SET) and (mark.floating is None):
            self.fixed_marks.append(mark)
        
    def plot_map(self):
        for mark in self.map_marks:
            mark.plot_mark()

    def marks_csv(self, csv_adress):
        """ Construct route from csv file"""
        marks_df = pd.read_csv(csv_adress, comment='#')
        marks_df = marks_df.replace('None',None)
        marks_df = marks_df.replace(np.nan,None)
        for i in range(len(marks_df)):
            mark_data = marks_df.loc[i]
            mark = Mark([float(mark_data[0]),float(mark_data[1])], mark_data[2], mark_data[3],
                    mark_data[4], mark_data[5], mark_data[6], mark_data[7])
            self.append_mark(mark)
                
    def compute_fixed_mark_disance(self, boat:Boat):
        for mark in self.fixed_marks:
            mark.compute_distance(boat)
            
    def sort_fixed_mark_distance(self):
        self.fixed_marks.sort(key=lambda x: x.distance)
        
    def select_near_fixed_marks(self, number: int):
        self.sort_fixed_mark_distance()
        best_marks = self.fixed_marks[0:number]
        return best_marks
        
    def __str__(self):
        map = ' '
        for mark in self.fixed_marks:
            map = map + mark.__str__()
        return map




class Route:
    """ append waypoints from a csv file to build a route"""
    # route obtained from openseamap, Fullscream chart, Tools, Trip planner, keep only latitude and longitude in decimal
    def __init__(self):
        self.route = []
        self.number_of_waypoint = 0
    
    def append_waypoint(self, waypoint:Waypoint):
        waypoint.waypoint_number = self.number_of_waypoint
        self.route.append(waypoint)
        self.number_of_waypoint += 1
        
    def plot_route(self):
        x = []
        y = []
        for point in self.route:
            x.append(point.position[0])
            y.append(point.position[1])
            plt.text(point.position[0], point.position[1], point.waypoint_number,
                     horizontalalignment='center',
                     verticalalignment='center',
                     color='w')
        plt.plot(x, y, '-o', markersize=15)
        

    def route_csv(self, csv_adress : str):
        """ Construct route from csv file"""
        route_csv = pd.read_csv(csv_adress, comment='#')
        for i in range(len(route_csv)):
            coordinate_x = route_csv.iloc[i,1]
            coordinate_y = route_csv.iloc[i,0]
            waypoint = Waypoint([coordinate_x, coordinate_y])
            self.append_waypoint(waypoint)
        
    def __str__(self):
        route = ' '
        for point in self.route:
            route = route + point.__str__()
        return route
                

def compute_intersection(mark1 : Mark, mark2 : Mark) -> list[float,float]:
    """ Compute intersection between two LOP of mark1 and mark2
    y = a1 x+ b1 (for LOP of mark1)
    y = a2 x+ b2 (for LOP of mark2)
    thus intersection at x = (b1-b2)/(a2-a1) """
    intersection_x = ((mark1.position[1] - 1/np.tan(mark1.bearing)*mark1.position[0])
            - (mark2.position[1] -1/np.tan(mark2.bearing)*mark2.position[0])) / ((1/np.tan(mark2.bearing)) - ( 1/np.tan(mark1.bearing)))
    intersection_y = 1/np.tan(mark1.bearing) * intersection_x + mark1.position[1] - 1/np.tan(mark1.bearing)*mark1.position[0]
    intersection = np.array([intersection_x, intersection_y])
    return intersection


def legend_unique():
    """ Remove duplicated labels """
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

def get_best_marks(mark_table) -> list[Mark, Mark, Mark]:
    """ Get the three best mark from a set of mark"""
    mark_table_size = len(mark_table)
    bearing_table = np.zeros((mark_table_size ,mark_table_size ))
    cost_table= np.zeros((mark_table_size ,mark_table_size ))
    cost_table2= np.zeros((mark_table_size ,mark_table_size ))

    for i , mark_i in enumerate(mark_table):
        for j, mark_j in enumerate(mark_table):
            bearing_table[i][j] = mark_j.bearing - mark_i.bearing

    cost_table = bearing_table % (2*np.pi)
    cost_table2 = - bearing_table % (2*np.pi)
    cost_table = np.minimum(cost_table,cost_table2)
    cost_table = cost_table - (2*np.pi/3)
    cost_table = abs(cost_table)

    comb = list(combinations(range(mark_table_size),3))

    min_cost = 1000.0
    index_min = 0
    for i, comb_i in enumerate(comb):
        cost=0
        for j in range(3):
            cost += cost_table[comb_i[j]][comb_i[(j+1)%3]]
        if cost < min_cost:
            min_cost = cost
            index_min = i

    mark_index = comb[index_min]

    return(mark_table[mark_index[0]], mark_table[mark_index[1]], mark_table[mark_index[2]])


def get_best_mark90(boat : Boat, mark_table):
    """ return the mark that is the closet to an 90 degree angle to boat course """
    bearing_table = np.zeros((len(mark_table),1),dtype=float)
    for i, amer in enumerate(mark_table):
        amer.compute_bearing(boat, 0)
        bearing_table[i]=amer.bearing

    bearing_table = boat.course - bearing_table

    cost_table = bearing_table % (2*np.pi)
    cost_table2 = - bearing_table % (2*np.pi)
    cost_table = np.minimum(cost_table,cost_table2)
    cost_table = cost_table - np.pi/2
    cost_table = abs(cost_table)

    index_min = np.array(cost_table).argmin()

    best_mark = mark_table[index_min.item()]
    return best_mark





def degree_minute_to_decimal(degree : int, minute : float):
    """ Convert degree minute to degree with decimal """
    return degree + minute/60


def main():
    plt.close('all')
    plt.figure(1)
    mark1 = Mark([100, 300], 'church')
    mark2 = Mark([500, 500], 'major_lighthouse')
    mark3 = Mark([500, 100], 'water_tower')
    boat_simu = BoatSimu([300, 310])
    mark1.plot_mark()
    mark2.plot_mark()
    mark3.plot_mark()

    boat_simu.compute_position_3lop(mark1,mark2,mark3)
    boat_simu.plot_boat()

    mark1.plot_mark_bearing(boat_simu.boat_true)
    mark2.plot_mark_bearing(boat_simu.boat_true)
    mark3.plot_mark_bearing(boat_simu.boat_true)
    
    #legend_unique()
    #plt.legend()

    plt.title("3 LOP position fix")
    plt.show()
    

if __name__ == "__main__":

    main()