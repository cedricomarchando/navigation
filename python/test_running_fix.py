""" test running fix"""
# %%

import numpy as np
import matplotlib.pyplot as plt
import navigation as nav


# %%

# initialisation
amer1 = nav.Amer(100,500,0,"Amer1")
boat = nav.Boat(300,310, course=np.pi/4, speed=100)
boat.plot_speed()

sigma = np.pi/90
amer1.compute_angle(boat, sigma)
amer1.plot_amer_angle(boat)

# use boat_temp to estimiate a boat position
boat_tmp = nav.Boat(amer1.x,amer1.y, course=amer1.angle + np.pi, speed = boat.speed)
boat_tmp.run(1)
boat_tmp.plot_position()

boat_tmp.course = boat.course
boat_tmp.run(1)
boat_tmp.plot_position()

amer_tmp = nav.Amer(boat_tmp.x, boat_tmp.y, amer1.angle, "amer_tmp")


#boat.run(1)
boat.plot_position()
boat.run(1)
boat.plot_position()

amer1.compute_angle(boat, 0)
amer1.plot_amer_angle(boat)


amer_tmp.plot_amer_angle(boat)



estimate = nav.compute_intersection(amer_tmp,amer1)
boat.x = estimate[0]
boat.y = estimate[1]
boat.plot_position()
plt.show()


# %%
