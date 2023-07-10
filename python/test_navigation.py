
# %%
import numpy as np
import matplotlib.pyplot as plt
import navigation as nav


# %%
plt.figure(1)
mark1 = nav.Mark([100,300], 'church')
mark2 = nav.Mark([500,500], 'lighthouse')
mark3 = nav.Mark([500,100], 'land_tower')
boat_simu = nav.BoatSimu([300,310])
mark1.plot_mark()
mark2.plot_mark()
mark3.plot_mark()

boat_simu.compute_position_3lop(mark1, mark2, mark3)

mark1.plot_mark_bearing(boat_simu.boat_true)
mark2.plot_mark_bearing(boat_simu.boat_true)
mark3.plot_mark_bearing(boat_simu.boat_true)
# circle1 = plt.Circle((position_x,position_y),radius, fill=False)
# plt.gca().add_patch(circle1)
boat_simu.plot_boat()
nav.legend_unique()
plt.draw()

# %%
plt.figure(2)
mark1 = nav.Mark([100,300], 'church')
mark2 = nav.Mark([500,500], 'lighthouse')
mark3 = nav.Mark([500,100], 'water_tower')
mark1.plot_mark()
mark2.plot_mark()
mark3.plot_mark()
for i in range(40,600,50):
    for j in range(150,590,100):
        boat_simu = nav.BoatSimu([i,j])
        boat_simu.compute_position_3lop(mark1, mark2, mark3)
        boat_simu.plot_boat()
        del boat_simu
nav.legend_unique()
plt.title("3 LOP position fix")
plt.draw()


# %% 2 LOP intersection
plt.figure(4)
mark1 = nav.Mark([100, 100], 'church')
mark2 = nav.Mark([500, 500], 'water_tower')
mark1.plot_mark()
mark2.plot_mark()

boat_simu = nav.BoatSimu([400,310])
boat_simu.compute_position_2lop(mark1, mark2, show_lop=True)
boat_simu.plot_boat()

nav.legend_unique()
plt.title("2 LOP fix")
plt.draw()

# %%
plt.figure(5)
mark1 = nav.Mark([100, 100], 'church')
mark2 = nav.Mark([500, 500], 'tower')
mark1.plot_mark()
mark2.plot_mark()
boat_simu = nav.BoatSimu([400,310])
boat_simu.plot_boat()

for i in range(100,600,50):
    for j in range(-100,i,50):
        boat_simu = nav.BoatSimu([i,j])
        boat_simu.compute_position_2lop(mark1, mark2,show_lop=False)
        boat_simu.plot_boat()
        del boat_simu
nav.legend_unique()
plt.title("2 LOP position fix")
plt.draw()

# %%
plt.figure(6)
sigma = np.pi/90 # 2 degree

mark1 = nav.Mark([100.0, 500.0])
mark2 = nav.Mark([500.0, 500.0])
mark3 = nav.Mark([500.0, 100.0])
mark4 = nav.Mark([100.0, 100.0])
mark5 = nav.Mark([250.0, 510.0])
mark1.plot_mark()
mark2.plot_mark()
mark3.plot_mark()
mark4.plot_mark()
mark5.plot_mark()
mark_table=[mark1, mark2, mark3, mark4, mark5]

for i in range(150,500,100):
    for j in range(150,500,100):
        boat_simu = nav.BoatSimu([i, j])
        for mark in mark_table:
            mark.compute_bearing(boat_simu.boat_true,sigma)
        markA, markB, markC = nav.get_best_marks(mark_table)
        boat_simu.compute_position_3lop(markA,markB,markC)
        boat_simu.plot_boat()
        markA.plot_mark_bearing(boat_simu.boat_true)
        markB.plot_mark_bearing(boat_simu.boat_true)
        markC.plot_mark_bearing(boat_simu.boat_true)
        del boat_simu

nav.legend_unique()
plt.show()

# %%




