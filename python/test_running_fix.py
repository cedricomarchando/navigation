""" test running fix"""
# %%
import numpy as np
import matplotlib.pyplot as plt
import navigation as nav

plt.figure(2)
sigma =  np.pi/180 # 2 degree

mark1 = nav.Mark([100.0, 400.0], 'church')
mark2 = nav.Mark([250.0, 510.0], 'lighthouse')
mark3 = nav.Mark([700.0, 400.0], 'major_lighthouse')
mark4 = nav.Mark([500.0, 100.0], 'land_tower')
mark5 = nav.Mark([200.0, 100.0], 'pillar','green')
mark6 = nav.Mark([50.0, 150.0], 'tower', 'east')

mark_table=[mark1, mark2, mark3, mark4, mark5, mark6]
for mark in mark_table:
    mark.plot_mark()

boat_simu = nav.BoatSimu([100,300],[100,300])
boat_simu.boat_true.ground_track.course = np.pi/2
boat_simu.boat_true.ground_track.speed = 100
boat_simu.boat_true.water_track.course = np.pi/2
boat_simu.boat_estimate.ground_track.course = np.pi/2
boat_simu.boat_estimate.ground_track.speed = 100
boat_simu.boat_estimate.water_track.course = np.pi/2


fix_period = 1
print(boat_simu.boat_true.ground_track)
boat_simu.boat_true.ground_track.plot_track()

boat_simu.plot_boat()

for i in range(8):
    best_mark = boat_simu.get_1best_mark(mark_table, fix_period)
    boat_simu.run_fix(best_mark, fix_period ,sigma, True)
    #boat_simu.run_fix(mark3, fix_period, sigma, True)
    boat_simu.plot_boat()


# boat_simu.run_fix(mark1,1,sigma)
# boat_simu.plot_boat()

plt.show()


# %%
