""" test running fix"""
# %%
import math
import matplotlib.pyplot as plt
import navigation as nav


plt.figure(2)
nav.Boat.markersize =30

boat = nav.Boat([100,300])
boat.ground_track.course = math.pi/4
boat.tide_track.course = 2*math.pi/4
boat.tide_track.speed = 50
boat.water_track.speed = 100



boat.tide_track.plot_track()

course_to_steer = boat.update_course_to_steer()
boat.water_track.course = course_to_steer
boat.plot_boat()
position_after_tide = boat.tide_track.run_track()
boat.water_track.start_position = position_after_tide

boat.water_track.plot_track()

boat.update_ground_speed()
boat.ground_track.plot_track()

plt.show()


# %%
