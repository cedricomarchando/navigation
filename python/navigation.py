# %%
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
from matplotlib.path import Path # For marker construction
import nautical_marker as  marker
import pandas as pd


class BoatSimu:
    """ BoatSimu class, 
    instantian Boat_true that represent the boat wit its true parameter
    and boat_estimate taht represent the boat with estimated parameters"""
    def __init__(self, true_x:float, true_y:float):
        self.boat_true = Boat( true_x, true_y)
        self.boat_estimate = Boat(true_x, true_y, color='r')

    def plot_boat(self):
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
        mark1_down = Mark(mark1_up.position_x, mark1_up.position_y)
        mark2_down = Mark(mark2_up.position_x, mark2_up.position_x)

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
            mark.position_x + self.boat_estimate.speed * duration * np.sin(self.boat_estimate.course),
            mark.position_y + self.boat_estimate.speed * duration * np.cos(self.boat_estimate.course),
            bearing = save_bearing
            )
        plt.plot(mark_tmp.position_x, mark_tmp.position_y,'+k', label ="mark shifted")

        mark_tmp.plot_mark_bearing(self.boat_true)

        estimate = compute_intersection(mark,mark_tmp)
        del mark_tmp
        self.boat_estimate.set_position(estimate)
        return estimate

class Boat:
    """ Boat class """
    def __init__(self,true_x, true_y,course = None,speed = None, color ='b'):
        self.true_x = true_x
        self.true_y = true_y
        self.speed = speed
        self.course = course
        self.color = color

    def plot_speed(self):
        """ Show speed with direction of course"""
        plt.arrow(self.true_x,self.true_y,
                  self.speed * np.sin(self.course),
                  self.speed * np.cos(self.course),
                  head_width = 10)

    def run(self,duration):
        """ Run with speed for a duration """
        self.true_x += self.speed * duration * np.sin(self.course)
        self.true_y += self.speed * duration * np.cos(self.course)

    def plot_position(self):
        """ Plot position """
        plt.plot(self.true_x, self.true_y, '^b', markerfacecolor='none', label='Boat position')

    def plot_boat(self,label = None):
        """ plot with a boat marker in the direction of the course """
        vertices = [(-2, 1), (1, 2), (3, 0), (1, -2), (-2, -1), (-2, 1)]
        codes = [1,3,2,3,1,79]
        boat_marker = Path(vertices,codes)
        if self.course is not None:
            angle = self.course - np.pi/2
            boat_marker = boat_marker.transformed(transforms.Affine2D().rotate(-angle))
        plt.plot(self.true_x, self.true_y, marker=boat_marker,
            markersize=10, color=self.color,  markerfacecolor='none',
            linestyle = 'None', label=label)

    def set_position(self,position):
        """ Set boat with new position """
        self.true_x = position[0]
        self.true_y = position[1]




class Mark:
    """ Mark class, including landmarks and Seamarks """
    def __init__(self,position_x, position_y, mark_type = 'lighthouse',  top_mark_type = None,
                 light_color = None, name = None, floating=False, show_top_mark=True, bearing = None, mark_number = None):
        self.position_x = position_x
        self.position_y = position_y
        self.mark_type = mark_type.lower()
        self.top_mark_type = top_mark_type
        self.light_color = light_color
        self.name = name
        self.floating = floating
        self.show_top_mark = show_top_mark
        self.bearing = bearing
        self.mark_number = mark_number

    def plot_position(self):
        """ Plot position"""
        #plt.plot(self.position_x, self.position_y,'*k', markersize = 10, label ="Mark")
        marker.PlotMark( self.position_x, self.position_y, self.mark_type, self.top_mark_type  )

    def plot_mark_bearing(self, boat):
        """ Plot LOP of a mark with dotted line"""
        x_line = np.linspace(self.position_x,boat.true_x,10)
        y_line = x_line * 1/np.tan(self.bearing) + self.position_y - self.position_x *  1/np.tan(self.bearing)
        plt.plot(x_line, y_line, '--k', linewidth=0.5, label = "Line of Position (LoP)")

    def compute_bearing(self, boat, sigma):
        """ compute Bearing angle of a mark from the point of vie of the Boat """
        vector_x = self.position_x - boat.true_x
        vector_y = self.position_y - boat.true_y
        bearing = np.arctan2(vector_x, vector_y)
        # bearing = bearing + random.normalvariate(mu=0.0,sigma = sigma)
        self.bearing = bearing + sigma
    
    def __str__(self):
        return f' x={self.position_x}, y={self.position_y}, mark_type={self.mark_type}, top_mark={self.top_mark_type}\n'


class MarksMap:
    """ Build map with all marks"""
    def __init__(self):
        self.marks_map = []
        self.number_of_marks = 0
    
    def append_mark(self, mark:Mark):
        mark.mark_number = self.number_of_marks
        self.marks_map.append(mark)
        self.number_of_marks += 1
        
    def plot_Map(self):
        for mark in self.marks_map:
            marker.PlotMark(mark.position_x, mark.position_y, mark.mark_type, mark.top_mark_type, mark.light_color,
                            mark.name, mark.floating, mark.show_top_mark)

    def marks_csv(self, csv_adress):
        """ Construct route from csv file"""
        marks_df = pd.read_csv(csv_adress)
        for i in range(len(marks_df)):
            mark_data = marks_df.loc[i]
            mark = Mark(float(mark_data[0]),float(mark_data[1]), mark_data[2], mark_data[3],
                    mark_data[4], mark_data[5], mark_data[6], mark_data[7])
            self.append_mark(mark)
        
    def __str__(self):
        map = ' '
        for mark in self.marks_map:
            map = map + mark.__str__()
        return map




class Waypoint:
    """ create a waypoint object """
    def __init__(self, position_x, position_y, course = None, waypoint_number = None):
        self.position_x = position_x
        self.position_y = position_y
        self.couse = course
        self.waypoint_number = waypoint_number
        
    def plot(self):
        plt.plot(self.position_x, self.position_y, 'o')
        
    def __str__(self):
        return f' id={self.waypoint_number}, x={self.position_x}, y={self.position_y} \n'
        

class Route:
    """ append waypoints from a csv file to build a route"""
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
            x.append(point.position_x)
            y.append(point.position_y)
            plt.text(point.position_x, point.position_y, point.waypoint_number,
                     horizontalalignment='center',
                     verticalalignment='center',
                     color='w')
        plt.plot(x, y, '-o', markersize=15)
        

    def route_csv(self, csv_adress):
        """ Construct route from csv file"""
        route_csv = pd.read_csv(csv_adress)
        for i in range(len(route_csv)):
            coordinate_x = route_csv.iloc[i,1]
            coordinate_y = route_csv.iloc[i,0]
            waypoint = Waypoint(coordinate_x, coordinate_y)
            self.append_waypoint(waypoint)
        
    def __str__(self):
        route = ' '
        for point in self.route:
            route = route + point.__str__()
        return route
                

def compute_intersection(mark1, mark2):
    """ Compute intersection between two LOP of mark1 and mark2"""
    # y = a1 x+ b1 (for LOP of mark1)
    # y = a2 x+ b2 (for LOP of mark2)
    #  thus intersection at x = (b1-b2)/(a2-a1)
    intersection_x = ((mark1.position_y - 1/np.tan(mark1.bearing)*mark1.position_x)
            - (mark2.position_y -1/np.tan(mark2.bearing)*mark2.position_x)) / ((1/np.tan(mark2.bearing)) - ( 1/np.tan(mark1.bearing)))
    intersection_y = 1/np.tan(mark1.bearing) * intersection_x + mark1.position_y - 1/np.tan(mark1.bearing)*mark1.position_x
    intersection = np.array([intersection_x, intersection_y])
    return intersection



def legend_unique():
    """ Remove duplicated labels """
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

def get_best_marks(mark_table):
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


def get_best_mark90(boat, mark_table):
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
    mark1 = Mark(100, 300, 'church')
    mark2 = Mark(500, 500, 'major_lighthouse')
    mark3 = Mark(500, 100, 'water_tower')
    boat_simu = BoatSimu(300,310)
    mark1.plot_position()
    mark2.plot_position()
    mark3.plot_position()

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