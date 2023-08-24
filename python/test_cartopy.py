# %%
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import nautical_marker as marker
import pandas as pd
import numpy as np
import navigation as nav



# rade.png obtained from OpenSeaMap
#img = plt.imread("../map/rade.png")
img = plt.imread('rade2.png')

# values for rade.png-3.3782, -3.33217, 47.715, 47.7309
lat_min = -3.37706
lat_max = -3.34298
long_min = 47.71285
long_max = 47.73366

img_extent = (lat_min, lat_max, long_min, long_max)

ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent( [lat_min, lat_max, long_min, long_max], crs=ccrs.PlateCarree())

plt.imshow(img, origin='upper', extent=img_extent, transform=ccrs.PlateCarree())
#plt.figure(figsize=(10, 5))



# %%
marker.PlotMark.markersize=30

marks_map = nav.MarksMap()
marks_map.marks_csv('marks.csv')
marks_map.plot_map()

routes = nav.Route()
routes.route_csv('./route.csv')
routes.plot_route()

print(routes.route[0])

sigma = np.pi/90 # 2 degree


SPEED = 0.1
FIX_PERIOD = 0.01

boat_simu = nav.BoatSimu(routes.route[0].position, routes.route[0].position)

boat_simu.set_tide_track(course=np.pi, speed=SPEED/3)

boat_simu.compute_waypoint_distance(routes.route[1])
print(f'distance_estimate:{boat_simu.boat_estimate.waypoint_distance} \t distance_true:{boat_simu.boat_true.waypoint_distance}')
boat_simu.boat_true.water_track.speed = SPEED
boat_simu.boat_estimate.water_track.speed = SPEED
boat_simu.boat_true.ground_track.speed = SPEED
boat_simu.boat_estimate.ground_track.speed = SPEED
boat_simu.plot_boat()
nearest_marks = boat_simu.select_near_fixed_marks(marks_map, sigma, 6)
boat_simu.update_2lop_fix(nearest_marks)

for route in routes.route:
    boat_simu.go_to_waypoint(route, marks_map, sigma, FIX_PERIOD, nav.FixType.FIX_3LOP)


#boat_simu.go_to_waypoint(route.route[2], marks_map, sigma, FIX_PERIOD, nav.FixType.FIX_3LOP)

plt.show()
# %%
