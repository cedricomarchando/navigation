""" test running fix"""
# %%
import numpy as np
import matplotlib.pyplot as plt
import navigation as nav

# %%

# initialisation
plt.figure(1)
mark = nav.Mark(200,500,'church')
mark.plot_position()
boat_simu = nav.BoatSimu(50,50)
boat_simu.boat_true.course=np.pi/2
boat_simu.boat_true.speed=100
boat_simu.boat_estimate.course=np.pi/2
boat_simu.boat_estimate.speed=100
boat_simu.plot_boat()

sigma = np.pi/180
mark.compute_bearing(boat_simu.boat_true, 0)
mark.plot_mark_bearing(boat_simu.boat_true)

for i in range(8):
    boat_simu.run_fix(mark,1,sigma)
    boat_simu.plot_boat()

nav.legend_unique()
plt.title("Running fix")
plt.draw()


# %%
plt.figure(2)
sigma = 0 # 2 degree

mark1 = nav.Mark(100.0, 500.0, 'church')
mark2 = nav.Mark(250.0, 510.0, 'lighthouse')
mark3 = nav.Mark(500.0, 500.0, 'major_lighthouse')
mark4 = nav.Mark(500.0, 100.0, 'land_tower')
mark5 = nav.Mark(200.0, 100.0, 'water_tower')
mark6 = nav.Mark(50.0, 150.0, 'tower', 'east')

mark_table=[mark1, mark2, mark3, mark4, mark5, mark6]
for mark in mark_table:
    mark.plot_position()

boat_simu = nav.BoatSimu(10,300)
boat_simu.boat_true.course=np.pi/2
boat_simu.boat_true.speed=100
boat_simu.boat_estimate.course=np.pi/2
boat_simu.boat_estimate.speed=100

boat_simu.plot_boat()
boat_simu.boat_true.plot_speed()

for i in range(8):
    best_mark = nav.get_best_mark90( boat_simu.boat_true, mark_table)
    boat_simu.run_fix(best_mark,1,sigma)
    boat_simu.plot_boat()


print(best_mark.mark_type)
plt.show()


# %%
