
# %%
import numpy as np
import matplotlib.pyplot as plt
import navigation as nav


# %%

amer1 = nav.Amer(100,300)
amer2 = nav.Amer(500,500)
amer3 = nav.Amer(500,100,0)
boat = nav.Boat(300,310)
amer1.plot_position()
amer2.plot_position()
amer3.plot_position()



estimate = nav.compute_position_3lop(boat,amer1,amer2,amer3)
boat.set_estimate(estimate)
boat.plot_position()

amer1.plot_amer_bearing(boat)
amer2.plot_amer_bearing(boat)
amer3.plot_amer_bearing(boat)
# circle1 = plt.Circle((position_x,position_y),radius, fill=False)
# plt.gca().add_patch(circle1)


nav.legend_unique()

plt.title("3 LOP position fix")
plt.show()


# %%

amer1 = nav.Amer(100,300)
amer2 = nav.Amer(500,500)
amer3 = nav.Amer(500,100)
amer1.plot_position()
amer2.plot_position()
amer3.plot_position()
for i in range(40,600,50):
    for j in range(150,590,100):
        boat = nav.Boat(i,j)
        estimate = nav.compute_position_3lop(boat,amer1,amer2,amer3)
        boat.set_estimate(estimate)
        boat.plot_position()
        del boat
nav.legend_unique()
plt.title("3 LOP position fix")
plt.show()

# %%

amer1 = nav.Amer(100,300)
amer2 = nav.Amer(400,100)
amer3 = nav.Amer(500,100)
amer1.plot_position()
amer2.plot_position()
amer3.plot_position()

for i in range(140,500,100):
    for j in range(120,500,100):
        boat = nav.Boat(i,j)
        estimate = nav.compute_position_3lop(boat,amer1,amer2,amer3)
        boat.set_estimate(estimate)
        boat.plot_position()
        del boat

nav.legend_unique()
plt.title("3 LOP position fix")
plt.show()

# %% 2 LOP intersection

amer1_up = nav.Amer(100,100)
amer2_up = nav.Amer(500,500)
amer1_up.plot_position()
amer2_up.plot_position()

boat = nav.Boat(400,310)
boat.plot_position()

nav.compute_position_2lop(boat,amer1_up,amer2_up,show_lop=True)

nav.legend_unique()
plt.title("2 LOP fix")
plt.show()

# %%
amer1_up = nav.Amer(100,100)
amer2_up = nav.Amer(500,500)
amer1_up.plot_position()
amer2_up.plot_position()
boat = nav.Boat(400,310)
boat.plot_position()

for i in range(100,600,50):
    for j in range(-100,i,50):
        boat = nav.Boat(i,j)
        boat.plot_position()
        nav.compute_position_2lop(boat,amer1_up,amer2_up,show_lop=False)
        del boat
nav.legend_unique()
plt.title("2 LOP position fix")
plt.show()

# %%
sigma = np.pi/90 # 2 degree

amer1 = nav.Amer(100.0, 500.0)
amer2 = nav.Amer(500.0, 500.0)
amer3 = nav.Amer(500.0, 100.0)
amer4 = nav.Amer(100.0, 100.0)
amer5 = nav.Amer(250.0, 510.0)
amer1.plot_position()
amer2.plot_position()
amer3.plot_position()
amer4.plot_position()
amer5.plot_position()
amer_table=[amer1, amer2, amer3, amer4, amer5]

for i in range(150,500,100):
    for j in range(150,500,100):
        boat = nav.Boat(i, j)
        for amer in amer_table:
            amer.compute_bearing(boat,sigma)
        amerA, amerB, amerC = nav.get_best_amers(amer_table)
        estimate = nav.compute_position_3lop(boat,amerA,amerB,amerC)
        boat.set_estimate(estimate)
        boat.plot_position()
        amerA.plot_amer_bearing(boat)
        amerB.plot_amer_bearing(boat)
        amerC.plot_amer_bearing(boat)

nav.legend_unique()
plt.show()

# %%




