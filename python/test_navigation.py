
# %%
import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations
import navigation as nav



# %%

amer1 = nav.Amer(100,300,0,"Amer1")
amer2 = nav.Amer(500,500,0,"Amer2")
amer3 = nav.Amer(500,100,0,"Amer3")
boat = nav.Boat(300,310)

position_x, position_y = nav.compute_position_3LOP(boat,amer1,amer2,amer3)

nav.plot_amer_angle(amer1,boat)
nav.plot_amer_angle(amer2,boat)
nav.plot_amer_angle(amer3,boat)
# circle1 = plt.Circle((position_x,position_y),radius, fill=False)
# plt.gca().add_patch(circle1)


nav.legend_unique()

plt.title("3 LOP position fix")
plt.show()


# %%

amer1 = nav.Amer(100,300,0,"Amer1")
amer2 = nav.Amer(500,500,0,"Amer2")
amer3 = nav.Amer(500,100,0,"Amer3")
for i in range(40,600,50):
    for j in range(150,590,100):
        boat = nav.Boat(i,j)
        position_x, position_y = nav.compute_position_3LOP(boat,amer1,amer2,amer3)
nav.legend_unique()
plt.title("3 LOP position fix")
plt.show()

# %%

amer1 = nav.Amer(100,300,0,"Amer1")
amer2 = nav.Amer(400,100,0,"Amer2")
amer3 = nav.Amer(500,100,0,"Amer3")

for i in range(140,500,100):
    for j in range(120,500,100):
        boat = nav.Boat(i,j)
        position_x, position_y = nav.compute_position_3LOP(boat,amer1,amer2,amer3)

nav.legend_unique()
plt.title("3 LOP position fix")
plt.show()

# %% 2 LOP intersection

amer1_up = nav.Amer(100,100,0,"Amer1_up")
amer2_up = nav.Amer(500,500,0,"Amer2_up")
boat = nav.Boat(400,310)

nav.compute_position_2LOP(boat,amer1_up,amer2_up,show_LOP=True)

nav.legend_unique()
plt.title("2 LOP fix")
plt.show()

# %%
amer1_up = nav.Amer(100,100,0,"Amer1_up")
amer2_up = nav.Amer(500,500,0,"Amer2_up")
boat = nav.Boat(400,310)

for i in range(100,600,50):
    for j in range(-100,i,50):
        boat = nav.Boat(i,j)
        nav.compute_position_2LOP(boat,amer1_up,amer2_up,show_LOP=False)

nav.legend_unique()
plt.title("2 LOP position fix")
plt.show()

# %%
sigma = np.pi/90 # 2 degree

amer1 = nav.Amer(100.0, 500.0, 0, "Amer1")
amer2 = nav.Amer(500.0, 500.0, 0, "Amer2")
amer3 = nav.Amer(500.0, 100.0, 0, "Amer3")
amer4 = nav.Amer(100.0, 100.0, 0, "Amer4")
amer5 = nav.Amer(250.0, 510.0, 0, "Amer5")
amer_table=[amer1, amer2, amer3, amer4, amer5]

for i in range(150,500,100):
    for j in range(150,500,100):
        boat = nav.Boat(i, j)
        for amer in amer_table:
            amer.angle  = nav.compute_angle(boat,amer,sigma)
        amerA, amerB, amerC = nav.get_best_amers(amer_table)   
        nav.compute_position_3LOP(boat,amerA,amerB,amerC)
        nav.plot_amer_angle(amerA,boat)
        nav.plot_amer_angle(amerB,boat)
        nav.plot_amer_angle(amerC,boat)

nav.legend_unique()
plt.show()

# %%




