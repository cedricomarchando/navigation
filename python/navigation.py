# %%
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt

#position fixing
# Line Of Position (LOP)

class Boat:
    """ Boat class """
    def __init__(self,true_x, true_y,estimate_x = None, estimate_y = None,course = None,speed = None):
        self.true_x = true_x
        self.true_y = true_y
        self.estimate_x = estimate_x
        self.estimate_y = estimate_y
        self.speed = speed
        self.course = course

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
        plt.plot(self.true_x,self.true_y,'^b', markerfacecolor='none', label='Boat position')
        if self.estimate_x is not None:
            plt.plot(self.estimate_x, self.estimate_y,'^r', markerfacecolor='none',label='Estimate')
    
    def set_position(self,position):
        """ Set bot with new position """
        self.true_x = position[0]
        self.true_y = position[1]
        
    def set_estimate(self,estimate):
        """ Set bot with new position """
        self.estimate_x = estimate[0]
        self.estimate_y = estimate[1]
        
    def run_fix(self,amer,duration,sigma):
        """ Run fix: get position from 1 amer and speed """
        save_bearing = amer.bearing
        # compute amer bearing after running
        self.run(duration)
        amer.compute_bearing(self, sigma)
        amer.plot_amer_bearing(self)
        # run amer in the direction of the boat
        duration = 1
        amer_tmp = Amer(
            amer.position_x + self.speed * duration * np.sin(self.course),
            amer.position_y + self.speed * duration * np.cos(self.course),
            save_bearing
            )
        plt.plot(amer_tmp.position_x, amer_tmp.position_y,'+k', label ="Amer shifted")

        amer_tmp.plot_amer_bearing(self)

        estimate = compute_intersection(amer,amer_tmp)
        del amer_tmp
        return estimate



class Amer:
    """ Amer class """
    def __init__(self,position_x,position_y,bearing = None, name = None):
        self.position_x = position_x
        self.position_y = position_y
        self.bearing = bearing
        self.name = name
        
    def plot_position(self):
        """ Plot position"""
        plt.plot(self.position_x, self.position_y,'*k', markersize = 10, label ="Amer")
    
       
    def plot_amer_bearing(self,boat):
        """ Plot LOP of an amer with dotted line"""
        x_line = np.linspace(self.position_x,boat.true_x,10)
        y_line = x_line * 1/np.tan(self.bearing) + self.position_y - self.position_x *  1/np.tan(self.bearing)
        plt.plot(x_line, y_line, '--k', linewidth=0.5, label = "Line of Position (LoP)")

    def compute_bearing(self,boat,sigma):
        """ compute Bearing angle of an Amer from the point of vie of the Boat """
        vector_x = self.position_x - boat.true_x
        vector_y = self.position_y - boat.true_y
        bearing = np.arctan2(vector_x, vector_y)
        # bearing = bearing + random.normalvariate(mu=0.0,sigma = sigma)
        self.bearing = bearing + sigma


def compute_intersection(amer1,amer2):
    """ Compute intersection between two LOP of amer1 and amer2"""
    # y = a1 x+ b1 (for LOP of amer1)
    # y = a2 x+ b2 (for LOP of amer2)
    #  thus intersection at x = (b1-b2)/(a2-a1)
    intersection_x = ((amer1.position_y - 1/np.tan(amer1.bearing)*amer1.position_x)
            - (amer2.position_y -1/np.tan(amer2.bearing)*amer2.position_x)) / ((1/np.tan(amer2.bearing)) - ( 1/np.tan(amer1.bearing)))
    intersection_y = 1/np.tan(amer1.bearing) * intersection_x + amer1.position_y - 1/np.tan(amer1.bearing)*amer1.position_x
    intersection = np.array([intersection_x, intersection_y])
    return intersection 


def compute_position_3lop(boat,amer1,amer2,amer3):
    """ Comput fix position with triangulation of 3LOP"""
    sigma = np.pi/90 # 2 degree
    amer1.compute_bearing(boat,sigma)
    amer2.compute_bearing(boat,sigma)
    amer3.compute_bearing(boat,sigma)
    intersection1 = compute_intersection(amer1,amer2)
    intersection2 = compute_intersection(amer2,amer3)
    intersection3 = compute_intersection(amer1,amer3)
    #compute barycentre using Chasles formula
    barycentre = (intersection1 + intersection2 + intersection3)/3
    #circonscribed_circle does not work
    plt.plot( (intersection1[0], intersection2[0], intersection3[0], intersection1[0]),
             (intersection1[1], intersection2[1], intersection3[1], intersection1[1]),'g')
    return barycentre

def compute_position_2lop(boat, amer1_up, amer2_up, show_lop):
    """ Compute estimated position with 2 LOP"""
    amer1_down = Amer(amer1_up.position_x, amer1_up.position_y,0,"Amer1_down")
    amer2_down = Amer(amer2_up.position_x, amer2_up.position_x,0,"Amer2_down")

    sigma = np.pi/90 # 2d egrees
    amer1_up.compute_bearing(boat,sigma)
    amer2_up.compute_bearing(boat,sigma)
    amer1_down.compute_bearing(boat,-sigma)
    amer2_down.compute_bearing(boat,-sigma)
    if show_lop:
        amer1_up.plot_amer_bearing(boat)
        amer2_up.plot_amer_bearing(boat)
        amer1_down.plot_amer_bearing(boat)
        amer2_down.plot_amer_bearing(boat)

    inter1 = compute_intersection(amer1_up,amer2_up)
    inter2 = compute_intersection(amer1_up,amer2_down)
    inter3 = compute_intersection(amer1_down,amer2_down)
    inter4 = compute_intersection(amer1_down,amer2_up)

    plt.plot( (inter1[0], inter2[0], inter3[0], inter4[0], inter1[0]),
            (inter1[1], inter2[1], inter3[1], inter4[1],  inter1[1]),'k')
    plt.fill( (inter1[0], inter2[0], inter3[0], inter4[0], inter1[0]),
            (inter1[1], inter2[1], inter3[1], inter4[1],  inter1[1]),'g',label="position area")


def legend_unique():
    """ Remove duplicated labels """
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

def get_best_amers(amer_table):
    """ Get the three best amer from a set of amer"""
    amer_table_size = len(amer_table)
    bearing_table = np.zeros((amer_table_size ,amer_table_size ))
    cost_table= np.zeros((amer_table_size ,amer_table_size ))
    cost_table2= np.zeros((amer_table_size ,amer_table_size ))

    for i , amer_i in enumerate(amer_table):
        for j, amer_j in enumerate(amer_table):
            bearing_table[i][j] = (amer_j.bearing - amer_i.bearing)

    cost_table = bearing_table % (2*np.pi)
    cost_table2 = - bearing_table % (2*np.pi)
    cost_table = np.minimum(cost_table,cost_table2)
    cost_table = cost_table - (2*np.pi/3)
    cost_table = abs(cost_table)

    comb = list(combinations(range(amer_table_size),3))

    min_cost = 1000.0
    index_min = 0
    for i, comb_i in enumerate(comb):
        cost=0
        for j in range(3):
            cost += cost_table[comb_i[j]][comb_i[(j+1)%3]]
        if cost < min_cost:
            min_cost = cost
            index_min = i

    amer_index = comb[index_min]

    return(amer_table[amer_index[0]], amer_table[amer_index[1]], amer_table[amer_index[2]])

# %%
