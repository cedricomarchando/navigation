""" test running fix"""
# %%
import numpy as np
import matplotlib.pyplot as plt
import navigation as nav

# %%

# initialisation
amer = nav.Amer(200,500,0,"Amer1")
amer.plot_position()
boat = nav.Boat(50,50, course=np.pi/4, speed=100)
boat.plot_position()

sigma = np.pi/180
amer.compute_bearing(boat, sigma)
amer.plot_amer_bearing(boat)

for i in range(8):
    estimate = boat.run_fix(amer,1,sigma)
    boat.set_estimate(estimate)
    boat.plot_position()


nav.legend_unique()
plt.title("Runnig fix")
plt.show()


# %%

sigma = 0 # 2 degree

amer1 = nav.Amer(100.0, 500.0)
amer2 = nav.Amer(250.0, 510.0)
amer3 = nav.Amer(500.0, 500.0)
amer4 = nav.Amer(500.0, 100.0)
amer5 = nav.Amer(200.0, 100.0)
amer6 = nav.Amer(50.0, 150.0)

amer1.plot_position()
amer2.plot_position()
amer3.plot_position()
amer4.plot_position()
amer5.plot_position()
amer6.plot_position()
amer_table=[amer1, amer2, amer3, amer4, amer5, amer6]


boat = nav.Boat(200,300, course=np.pi/2, speed=100)
boat.plot_position()
boat.plot_speed()

# build cost table such that lowest cost is + or - pi/2 angle
bearing_table = np.zeros((len(amer_table),1),dtype=float)
for i, amer in enumerate(amer_table):
    amer.compute_bearing(boat,sigma)
    bearing_table[i]=amer.bearing

bearing_table = boat.course - bearing_table
print(bearing_table)
# bearing_table = abs(bearing_table)
# print(bearing_table)
#bearing_table = bearing_table - np.pi/4
#print(bearing_table)

plt.show()


# %%
