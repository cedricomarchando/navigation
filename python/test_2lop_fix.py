""" test running fix"""
# %%
import numpy as np
import matplotlib.pyplot as plt
import navigation as nav


# %%
plt.figure(6)
sigma = np.pi/90 # 2 degree

mark1 = nav.Mark([100.0, 500.0], 'church')
mark2 = nav.Mark([250.0, 510.0], 'lighthouse')
mark3 = nav.Mark([500.0, 500.0], 'land_tower')
mark4 = nav.Mark([500.0, 100.0], 'water_tower')
mark5 = nav.Mark([100.0, 100.0])

mark1.plot_mark()
mark2.plot_mark()
mark3.plot_mark()
mark4.plot_mark()
mark5.plot_mark()
mark_table=[mark1, mark2, mark3, mark4, mark5]

for i in range(0,700,100):
    for j in range(50,600,100):
        boat_simu = nav.BoatSimu([i, j], [i, j])
        for mark in mark_table:
            mark.compute_bearing(boat_simu.boat_true,sigma)
        markA, markB = boat_simu.get_2best_marks(mark_table)
        boat_simu.compute_position_2lop(markA, markB, show_lop=True)
        boat_simu.plot_boat()
        del boat_simu
        
# boat_simu = nav.BoatSimu([200, 300])
# markA, markB = boat_simu.get_2best_marks(mark_table)
# boat_simu.compute_position_2lop(markA, markB, show_lop=True)
#boat_simu.plot_boat()

nav.legend_unique()
plt.show()

# %%
