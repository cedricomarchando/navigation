""" test running fix"""
# %%

import copy
import numpy as np
import matplotlib.pyplot as plt
import navigation as nav



# %%

# initialisation
amer1 = nav.Amer(100,500,0,"Amer1")
amer1.plot_position()
boat = nav.Boat(300,310, course=np.pi/4, speed=150)
boat.plot_position()

sigma = np.pi/90
amer1.compute_angle(boat, sigma)
amer1.plot_amer_angle(boat)

amer_save = copy.deepcopy(amer1)
boat_save = copy.deepcopy(boat)
amer_tmp = nav.Amer(boat_save.true_x, boat_save.true_y, boat_save.course)

# compute amer1 angle after running
boat.run(1)
amer1.compute_angle(boat, sigma)
amer1.plot_amer_angle(boat)


# use boat_temp to estimiate a boat position

estimate = nav.compute_intersection(amer_save,amer_tmp) # set boat on LOP
boat_save.set_position(estimate)
boat_save.run(1)
boat_save.angle = amer_save.angle
amer_tmp2 = nav.Amer(boat_save.true_x, boat_save.true_y, boat_save.course)



estimate = nav.compute_intersection(amer1,amer_tmp2)

del amer_save
del boat_save
del amer_tmp
del amer_tmp2
plt.plot(estimate[0], estimate[1],'^r', markerfacecolor='none',label='Estimate')
boat.plot_position()

plt.show()


# %%
