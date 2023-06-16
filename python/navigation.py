# %%
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

#position fixing
# Line Of Position (LOP)


class Boat:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        plt.plot(self.x,self.y,'^b', markerfacecolor='none', label='Boat position')

class Amer:
    def __init__(self,x,y,angle,name):
        self.x=x
        self.y=y
        self.angle = angle
        self.name = name
        plt.plot(self.x,self.y,'*k', markersize = 10, label ="Amer")

def compute_angle(amer,boat,sigma):
    x = amer.x - boat.x
    y = amer.y - boat.y
    angle = np.arctan2(x,y)
    # angle = angle + random.normalvariate(mu=0.0,sigma = sigma)
    angle = angle + sigma
    return angle


def plot_amer_angle(amer,boat):
    x = np.linspace(amer.x,boat.x,10) 
    y = x * 1/np.tan(amer.angle) + amer.y - amer.x *  1/np.tan(amer.angle)
    plt.plot(x,y,'--k',linewidth=0.5, label = "Line of Position (LoP)")

def compute_intersection(amer1,amer2):
    # put in the form AX = B, then solve X=inv(A).B
    # the line  of an amer is given by y= x/tang(alpha)  + amer.y - amer.x/tang(alpha)
    A = np.array([[-1/np.tan(amer1.angle) , 1],
                  [-1/np.tan(amer2.angle) , 1]])
    B = [[amer1.y - 1/np.tan(amer1.angle)*amer1.x],
       [amer2.y -1/np.tan(amer2.angle)*amer2.x]]
    X = np.linalg.inv(A).dot(B)
    return(X)

def compute_position_3LOP(boat,amer1,amer2,amer3):
    sigma = np.pi/90 # 2 degree
    amer1.angle  = compute_angle(boat,amer1,sigma)
    amer2.angle  = compute_angle(boat,amer2,sigma)
    amer3.angle  = compute_angle(boat,amer3,sigma)
    intersection1 = compute_intersection(amer1,amer2)
    intersection2 = compute_intersection(amer2,amer3)
    intersection3 = compute_intersection(amer1,amer3)
    #compute barycentre using Chasles formula
    barycentre = (intersection1 + intersection2 + intersection3)/3
    #circonscribed_circle does not work
    plt.plot( (intersection1[0], intersection2[0], intersection3[0], intersection1[0]),
             (intersection1[1], intersection2[1], intersection3[1], intersection1[1]),'g')
    plt.plot(barycentre[0], barycentre[1],'^r', markerfacecolor='none',label='Estimate')
    return barycentre[0], barycentre[1]

def compute_position_2LOP(boat, amer1_up, amer2_up, show_LOP):
    amer1_down = Amer(amer1_up.x,amer1_up.y,0,"Amer1_down")
    amer2_down = Amer(amer2_up.x,amer2_up.x,0,"Amer2_down")

    sigma = np.pi/90 # 2d egrees
    amer1_up.angle  = compute_angle(boat,amer1_up,sigma)
    amer2_up.angle  = compute_angle(boat,amer2_up,sigma)
    amer1_down.angle  = compute_angle(boat,amer1_down,-sigma)
    amer2_down.angle  = compute_angle(boat,amer2_down,-sigma)
    
    if show_LOP:
        plot_amer_angle(amer1_up,boat)
        plot_amer_angle(amer2_up,boat)
        plot_amer_angle(amer1_down,boat)
        plot_amer_angle(amer2_down,boat)    

    inter1 = compute_intersection(amer1_up,amer2_up)
    inter2 = compute_intersection(amer1_up,amer2_down)
    inter3 = compute_intersection(amer1_down,amer2_down)
    inter4 = compute_intersection(amer1_down,amer2_up)

    plt.plot( (inter1[0], inter2[0], inter3[0], inter4[0], inter1[0]),
            (inter1[1], inter2[1], inter3[1], inter4[1],  inter1[1]),'k')
    plt.fill( (inter1[0], inter2[0], inter3[0], inter4[0], inter1[0]),
            (inter1[1], inter2[1], inter3[1], inter4[1],  inter1[1]),'g',label="position area")


def legend_unique(): # Remove duplicated labels
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    

def get_best_amers(amer_table):

    amer_table_size = len(amer_table)
    angle_table = np.zeros((amer_table_size ,amer_table_size ))
    cost_table= np.zeros((amer_table_size ,amer_table_size ))
    cost_table2= np.zeros((amer_table_size ,amer_table_size ))

    for i , amer_i in enumerate(amer_table):
        for j, amer_j in enumerate(amer_table):
            angle_table[i][j] = (amer_j.angle - amer_i.angle)

    cost_table = angle_table % (2*np.pi)
    cost_table2 = - angle_table % (2*np.pi)
    cost_table = np.minimum(cost_table,cost_table2)
    cost_table = cost_table - (2*np.pi/3)
    cost_table = abs(cost_table)
    print("cost_table")

    comb = list(combinations(range(amer_table_size),3))

    min_cost = 1000.0
    index_min = 0
    for i, comb_i in enumerate(comb):
        cost=0
        print(comb_i)
        for j in range(3):
            cost += cost_table[comb_i[j]][comb_i[(j+1)%3]]
        if cost < min_cost:
            min_cost = cost
            index_min = i
        print(cost)

    amer_index = comb[index_min]
    print(amer_index)

    return(amer_table[amer_index[0]], amer_table[amer_index[1]], amer_table[amer_index[2]])


# %%

amer1 = Amer(100,300,0,"Amer1")
amer2 = Amer(500,500,0,"Amer2")
amer3 = Amer(500,100,0,"Amer3")
boat = Boat(300,310)

position_x, position_y = compute_position_3LOP(boat,amer1,amer2,amer3)

plot_amer_angle(amer1,boat)
plot_amer_angle(amer2,boat)
plot_amer_angle(amer3,boat)
# circle1 = plt.Circle((position_x,position_y),radius, fill=False)
# plt.gca().add_patch(circle1)


legend_unique()
plt.title("3 LOP position fix")
plt.show()


# %%

amer1 = Amer(100,300,0,"Amer1")
amer2 = Amer(500,500,0,"Amer2")
amer3 = Amer(500,100,0,"Amer3")
for i in range(40,600,50):
    for j in range(150,590,100):
        boat = Boat(i,j)
        position_x, position_y = compute_position_3LOP(boat,amer1,amer2,amer3)
legend_unique()
plt.title("3 LOP position fix")
plt.show()

# %%

amer1 = Amer(100,300,0,"Amer1")
amer2 = Amer(400,100,0,"Amer2")
amer3 = Amer(500,100,0,"Amer3")

for i in range(140,500,100):
    for j in range(120,500,100):
        boat = Boat(i,j)
        position_x, position_y = compute_position_3LOP(boat,amer1,amer2,amer3)

legend_unique()
plt.title("3 LOP position fix")
plt.show()

# %% 2 LOP intersection

amer1_up = Amer(100,100,0,"Amer1_up")
amer2_up = Amer(500,500,0,"Amer2_up")
boat = Boat(400,310)

compute_position_2LOP(boat,amer1_up,amer2_up,show_LOP=True)

legend_unique()
plt.title("2 LOP fix")
plt.show()

# %%
amer1_up = Amer(100,100,0,"Amer1_up")
amer2_up = Amer(500,500,0,"Amer2_up")
boat = Boat(400,310)

for i in range(100,600,50):
    for j in range(-100,i,50):
        boat = Boat(i,j)
        compute_position_2LOP(boat,amer1_up,amer2_up,show_LOP=False)

legend_unique()
plt.title("2 LOP position fix")
plt.show()

# %%
sigma = np.pi/90 # 2 degree

amer1 = Amer(100.0, 500.0, 0, "Amer1")
amer2 = Amer(500.0, 500.0, 0, "Amer2")
amer3 = Amer(500.0, 100.0, 0, "Amer3")
amer4 = Amer(100.0, 100.0, 0, "Amer4")
amer5 = Amer(250.0, 510.0, 0, "Amer5")
amer_table=[amer1, amer2, amer3, amer4, amer5]

for i in range(150,500,100):
    for j in range(150,500,100):
        boat = Boat(i, j)
        for amer in amer_table:
            amer.angle  = compute_angle(boat,amer,sigma)
        amerA, amerB, amerC = get_best_amers(amer_table)   
        compute_position_3LOP(boat,amerA,amerB,amerC)
        plot_amer_angle(amerA,boat)
        plot_amer_angle(amerB,boat)
        plot_amer_angle(amerC,boat)

legend_unique()
plt.show()

# %%
