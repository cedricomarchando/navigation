""" test running fix"""
# %%
import math
import matplotlib.pyplot as plt
import navigation as nav


plt.figure(2)
nav.Boat.markersize =30

SPEED = 100


boat_simu = nav.BoatSimu([100,300],[100,300])

boat_simu.set_tide_track(course=0*math.pi/2, speed=SPEED/2)
boat = boat_simu.boat_true
boat.ground_track.course = math.pi/4
boat.water_track.speed = SPEED



boat.tide_track.plot_track()

boat.update_course_to_steer()
boat.update_ground_speed()

boat.ground_track.plot_track()

# plot water track
position_after_tide = boat.tide_track.run_track()
boat.water_track.start_position = position_after_tide
boat.water_track.plot_track()

boat.plot_boat()
plt.legend()
plt.show()


# %%
