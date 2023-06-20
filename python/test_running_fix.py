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
amer.compute_angle(boat, sigma)
amer.plot_amer_angle(boat)

for i in range(8):
    estimate = boat.run_fix(amer,1,sigma)
    boat.set_estimate(estimate)
    boat.plot_position()


nav.legend_unique()
plt.title()
plt.show()


# %%
