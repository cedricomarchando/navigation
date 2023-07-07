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

route = nav.Route()
route.route_csv('./route.csv')
route.plot_route()

print(route.route[0])

sigma = np.pi/90 # 2 degree
boat_simu = nav.BoatSimu(route.route[0].position_x, route.route[0].position_y)
boat_simu.boat_true.course = route.route[0].course
boat_simu.boat_true.speed = 0.1
boat_simu.boat_estimate.course = route.route[0].course
boat_simu.boat_estimate.speed = 0.1


boat_simu.run(0.01)
boat_simu.update_3lop_fix(marks_map, sigma)
boat_simu.run(0.01)
boat_simu.update_3lop_fix(marks_map, sigma)
boat_simu.run(0.01)
boat_simu.update_3lop_fix(marks_map, sigma)
plt.show()
# %%
