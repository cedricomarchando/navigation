# %%
from itertools import combinations
from enum import Enum, auto
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
from matplotlib.path import Path # For marker construction
import nautical_marker as  marker
import pandas as pd
from shapely.geometry import Polygon
import shapely


class FixType(Enum):
    FIX_3LOP = auto()
    FIX_2LOP = auto()
    FIX_RUNNING = auto()
    
    
class Waypoint:
    """ create a waypoint object """
    def __init__(self, position :list[float, float], waypoint_number: int = None):
        self.position = position
        self.waypoint_number = waypoint_number
        
    def plot(self):
        plt.plot(self.position[0], self.position[1], 'o')
        
    def __str__(self):
        return f' x={self.position[0]}, y={self.position[1]}, waypoint_id={self.waypoint_number}\n'

class Boat:
    """ Boat class """
    def __init__(self, position :list[float, float], course:float = None, speed:float = None, waypoint_distance:float = None, color ='b'):
        self.position = position
        self.speed = speed
        self.course = course
        self.color = color
        self.waypoint_distance = waypoint_distance

    def plot_speed(self):
        """ Show speed with direction of course"""
        plt.arrow(self.position[0],
                  self.position[1],
                  self.speed * np.sin(self.course),
                  self.speed * np.cos(self.course),
                  head_width = 10)

    def run(self,duration:float):
        """ Run with speed for a duration """
        self.position[0] += self.speed * duration * np.sin(self.course)
        self.position[1] += self.speed * duration * np.cos(self.course)

    def plot_position(self):
        """ Plot position """
        plt.plot(self.position[0], self.position[1], '^b', markerfacecolor='none', label='Boat position')

    def plot_boat(self):
        """ plot with a boat marker in the direction of the course """
        vertices = [(-2, 1), (1, 2), (3, 0), (1, -2), (-2, -1), (-2, 1)]
        codes = [1,3,2,3,1,79]
        boat_marker = Path(vertices,codes)
        if self.course is not None:
            angle = self.course - np.pi/2
            boat_marker = boat_marker.transformed(transforms.Affine2D().rotate(-angle))
        plt.plot(self.position[0], self.position[1], marker=boat_marker,
            markersize=10, color=self.color,  markerfacecolor='none',
            linestyle = 'None')

    def set_position(self,position : list[float, float]) -> None:
        """ Set boat with new position """
        self.position = position
 
    def set_waypoint_course(self, position :list[float, float]) -> None:
        """ give course to go to position """
        vector_x = position[0] - self.position[0]
        vector_y = position[1] - self.position[1]
        self.course = np.arctan2(vector_x, vector_y)

    def compute_waypoint_distance(self, waypoint:Waypoint) -> float:
        self.waypoint_distance = math.dist(self.position, waypoint.position)

    def get_1best_mark90(self, mark_table:'MarksMap'):
        """ return the mark that is the closet to an 90 degree angle to boat course """
        bearing_table = np.zeros((len(mark_table),1),dtype=float)
        for i, amer in enumerate(mark_table):
            amer.compute_bearing(self, 0)
            bearing_table[i]=amer.bearing
        bearing_table = self.course - bearing_table
        cost_table = bearing_table % (2*np.pi)
        cost_table2 = - bearing_table % (2*np.pi)
        cost_table = np.minimum(cost_table,cost_table2)
        cost_table = cost_table - np.pi/2
        cost_table = abs(cost_table)

        index_min = np.array(cost_table).argmin()

        best_mark = mark_table[index_min.item()]
        return best_mark

    def __str__(self):
        return (f' x={self.position[0]}, y={self.position[1]}, speed={self.speed},'
                f' course={self.course}, waypoint_disatance={self.waypoint_distance} \n')





class Mark:
    """ Mark class, including landmarks and Seamarks """
    def __init__(self,position :list[float, float], mark_type = 'lighthouse',  top_mark_type = None,
                 light_color = None, name = None, floating:bool=False, show_top_mark:bool=True, bearing = None, distance = None):
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
        lop = self.bearing - np.pi
        x_line = (self.position[0] + np.sin(lop) *
                  math.dist(self.position,boat.position))
        y_line = (self.position[1] + np.cos(lop) *
                  math.dist(self.position,boat.position))
        plt.plot([self.position[0], x_line],
                 [self.position[1], y_line],
                 '--k', linewidth=0.5)

    def polygone_estimate(self, boat:Boat, sigma):
        """ build triangle of possible boat estimated position """
        point_a = tuple(self.position)
        point_b_x = (self.position[0] +
                     np.sin(self.bearing - np.pi + sigma) *
                     math.dist(self.position, boat.position) * 2)
        point_b_y = (self.position[1] +
                     np.cos(self.bearing - np.pi + sigma) *
                     math.dist(self.position, boat.position) * 2)
        point_b = (point_b_x, point_b_y)
        point_c_x = (self.position[0]
                     + np.sin(self.bearing - np.pi - sigma) *
                     math.dist(self.position, boat.position) * 2)
        point_c_y = (self.position[1]
                     + np.cos(self.bearing - np.pi - sigma) *
                     math.dist(self.position, boat.position) * 2)
        point_c = (point_c_x, point_c_y)
        return point_a, point_b, point_c

    def compute_bearing(self, boat:Boat, sigma: float):
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
                f'name={self.name}, floating={self.floating}, bearing={self.bearing}, distance={self.distance}\n')

class MarksMap:
    """ Build map with all marks"""
    def __init__(self):
        self.map_marks : list[Mark] = []
        self.fixed_marks : list[Mark] = []

    def append_mark(self, mark:Mark):
        self.map_marks.append(mark)
        if mark.mark_type in marker.LANDMARKS_SET:
            self.fixed_marks.append(mark)
        if (mark.mark_type in marker.SEAMARK_SET) and (mark.floating is None):
            self.fixed_marks.append(mark)

    def plot_map(self):
        for mark in self.map_marks:
            mark.plot_mark()

    def marks_csv(self, csv_adress: str):
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





class BoatSimu:
    """ BoatSimu class, 
    instantian Boat_true that represent the boat wit its true parameter
    and boat_estimate taht represent the boat with estimated parameters"""
    def __init__(self, true_position:list[float, float],estimate_position: list[float, float]):
        self.boat_true = Boat( true_position, color='g')
        self.boat_estimate = Boat( estimate_position, color='r')

    def plot_boat(self) ->None:
        " plot boat true and boat estimate"
        self.boat_true.plot_boat()
        self.boat_estimate.plot_boat()

    def compute_position_3lop(self, mark1, mark2, mark3, show_lop):
        """ Comput fix position with triangulation of 3 Lines Of Position (LOP) """
        sigma = np.pi/90 # 2 degree
        mark1.compute_bearing(self.boat_true,0)
        mark2.compute_bearing(self.boat_true,0)
        mark3.compute_bearing(self.boat_true,0)
        if show_lop:
            mark1.plot_mark_bearing(self.boat_true)
            mark2.plot_mark_bearing(self.boat_true)
            mark3.plot_mark_bearing(self.boat_true)
        poly_intersection = self.compute_intersection_3lop(mark1, mark2, mark3, sigma)
        if poly_intersection.is_empty:
            print(f'empty intersection for boat at position \n{self.boat_true.position}')
            barycentre = [0.0, 0.0]
        else:
            x, y = poly_intersection.exterior.xy
            plt.plot(x,y, c='g')
            barycentre = shapely.get_coordinates(poly_intersection.centroid).tolist()[0]
        self.boat_estimate.set_position(barycentre)   
        return barycentre

    def compute_position_2lop(self, mark1:Mark, mark2:Mark, show_lop:bool):
        """ Compute estimated position with 2 LOP"""
        sigma = np.pi/90 # 2d egrees
        mark1.compute_bearing(self.boat_true,0)
        mark2.compute_bearing(self.boat_true,0)
        if show_lop:
            mark1.plot_mark_bearing(self.boat_true)
            mark2.plot_mark_bearing(self.boat_true)
        poly_intersection = self.compute_intersection_2lop(mark1, mark2, sigma)
        if poly_intersection.is_empty:
            print(f'empty intersection for boat at position \n{self.boat_true.position}')
            barycentre = [0.0, 0.0]
        else:
            x, y = poly_intersection.exterior.xy
            plt.plot(x,y, c='g')
            barycentre = shapely.get_coordinates(poly_intersection.centroid).tolist()[0]
        self.boat_estimate.set_position(barycentre)
        return barycentre
    
    def compute_intersection_2lop(self, mark1:Mark, mark2:Mark, sigma:float):
        """ compute intersection of two polygones"""
        poly_tuple1 = mark1.polygone_estimate(self.boat_true, sigma)
        polygone1 = Polygon(poly_tuple1)
        poly_tuple2 = mark2.polygone_estimate(self.boat_true, sigma)
        polygone2 = Polygon(poly_tuple2)
        poly_intersection = polygone1.intersection(polygone2)
        return poly_intersection
    
    def compute_intersection_3lop(self, mark1:Mark, mark2:Mark, mark3:Mark, sigma:float):
        """ compute intersection of two polygones"""
        polygone_2lop = self.compute_intersection_2lop(mark1, mark2, sigma)
        poly_tuple3 = mark3.polygone_estimate(self.boat_true, sigma)
        polygone3 = Polygon(poly_tuple3)        
        polygone_3lop = polygone_2lop.intersection(polygone3)
        return polygone_3lop
    
        
    def get_2best_marks(self, mark_table:MarksMap) -> tuple():
        """ Get the two best mark from a set of mark, considering area of intersection"""
        sigma = np.pi/90 # 2d egrees
        for i, mark in enumerate(mark_table):
            mark.compute_bearing(self.boat_true, 0)
        comb = list(combinations(range(len(mark_table)), 2))
        min_cost = 100000
        for i, comb_i in enumerate(comb):
            poly_intersection = self.compute_intersection_2lop(
                mark_table[comb_i[0]], mark_table[comb_i[1]], sigma)
            cost = poly_intersection.area
            if cost < min_cost:
                min_cost = cost
                index_min = i
        mark_index = comb[index_min]
        return mark_table[mark_index[0]], mark_table[mark_index[1]]
    
    def get_3best_marks(self, mark_table:MarksMap) -> tuple():
        """ Get the three best mark from a set of mark, considering area of intersection """
        sigma = np.pi/90 # 2d egrees
        for i, mark in enumerate(mark_table):
            mark.compute_bearing(self.boat_true, 0)
        comb = list(combinations(range(len(mark_table)), 3))
        min_cost = 100000
        for i, comb_i in enumerate(comb):
            poly_intersection = self.compute_intersection_3lop(
                mark_table[comb_i[0]], mark_table[comb_i[1]],  mark_table[comb_i[2]], sigma)
            cost = poly_intersection.area
            if cost < min_cost:
                min_cost = cost
                index_min = i
        mark_index = comb[index_min]
        return mark_table[mark_index[0]], mark_table[mark_index[1]], mark_table[mark_index[2]]

    
    def run_fix(self, mark:Mark, fix_period:float, sigma:float):
        """ Run fix: get position from 1 mark and speed """
        mark.compute_bearing(self.boat_true, sigma)
        save_bearing = mark.bearing
        print(self.boat_estimate.position)
        print(self.boat_true.position)
        # compute updated bearing after running
        self.run(fix_period)
        
        print(self.boat_estimate.position)
        print(self.boat_true.position)
        
        mark.compute_bearing(self.boat_true, sigma)
        mark.plot_mark_bearing(self.boat_true)
        # run mark in the direction of the boat
        mark_shifted = Mark(
            [mark.position[0] + self.boat_estimate.speed * fix_period * np.sin(self.boat_estimate.course),
            mark.position[1] + self.boat_estimate.speed * fix_period * np.cos(self.boat_estimate.course)],
            bearing = save_bearing
            )
        plt.plot(mark_shifted.position[0], mark_shifted.position[1],'+k')
        mark_shifted.plot_mark_bearing(self.boat_true)
        estimate = compute_intersection(mark,mark_shifted)
        del mark_shifted
        self.boat_estimate.set_position(estimate)
        
        print(self.boat_estimate.position)
        print(self.boat_true.position)
        
        return estimate

    def update_3lop_fix(self, nearest_marks: Mark) -> None:
        markA, markB, markC = self.get_3best_marks(nearest_marks)
        self.compute_position_3lop(markA, markB, markC, show_lop=False)

    def update_2lop_fix(self, nearest_marks: Mark) -> None:
        markA, markB = self.get_2best_marks(nearest_marks)
        self.compute_position_2lop(markA, markB, show_lop=False)

    def update_run_fix(self, nearest_marks: Mark, fix_period: float, sigma: float) -> None:
        best_mark = self.boat_true.get_1best_mark90(nearest_marks)
        self.run_fix(best_mark, fix_period, sigma)

    def run(self,duration : float):
        self.boat_estimate.run(duration)
        self.boat_true.run(duration)

    def set_waypoint_course(self, position: list[float, float]):
        self.boat_estimate.set_waypoint_course(position)
        self.boat_true.set_waypoint_course(position)

    def compute_waypoint_distance(self, waypoint:Waypoint) -> None:
        self.boat_estimate.compute_waypoint_distance(waypoint)
        self.boat_true.compute_waypoint_distance(waypoint)

    def select_near_fixed_marks(self, marks_map:MarksMap, sigma: float, number_of_marks: int):
        marks_map.compute_fixed_mark_disance(self.boat_estimate)
        nearest_marks = marks_map.select_near_fixed_marks(number_of_marks)
        for mark in nearest_marks:
            mark.compute_bearing(self.boat_true, sigma)
        return nearest_marks

    def go_to_waypoint(self, waypoint:Waypoint, marks_map:MarksMap, sigma:float, fix_period:float, fix_type:FixType):
        self.compute_waypoint_distance(waypoint)
        #while self.boat_estimate.waypoint_distance > self.boat_estimate.speed * fix_period:
        while self.boat_true.waypoint_distance > self.boat_true.speed * fix_period:
            self.set_waypoint_course(waypoint.position) 
            nearest_marks = self.select_near_fixed_marks(marks_map, sigma, 6)
            match fix_type:
                case FixType.FIX_2LOP:
                    self.run(fix_period)
                    self.update_2lop_fix(nearest_marks)
                case FixType.FIX_3LOP:
                    self.run(fix_period)
                    self.update_3lop_fix(nearest_marks)
                case FixType.FIX_RUNNING:
                    self.update_run_fix(nearest_marks, fix_period, sigma)     
            self.plot_boat()
            self.compute_waypoint_distance(waypoint)


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
        waypoints_x = []
        waypoints_y = []
        for point in self.route:
            waypoints_x.append(point.position[0])
            waypoints_y.append(point.position[1])
            plt.text(point.position[0], point.position[1], point.waypoint_number,
                     horizontalalignment='center',
                     verticalalignment='center',
                     color='w')
        plt.plot(waypoints_x, waypoints_y, '-o', markersize=15)

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


def degree_minute_to_decimal(degree : int, minute : float):
    """ Convert degree minute to degree with decimal """
    return degree + minute/60


def main():
    plt.close('all')
    plt.figure(1)
    mark1 = Mark([100, 300], 'church')
    mark2 = Mark([500, 500], 'major_lighthouse')
    mark3 = Mark([500, 100], 'water_tower')
    boat_simu = BoatSimu([300, 310],[300, 310])
    mark1.plot_mark()
    mark2.plot_mark()
    mark3.plot_mark()

    boat_simu.compute_position_3lop(mark1, mark2, mark3, show_lop=True)
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