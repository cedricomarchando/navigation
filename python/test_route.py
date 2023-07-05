# %%
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import nautical_marker as marker
import navigation as nav
import pandas as pd

# %%

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


# route obtained from openseamap, Fullscream chart, Tools, Trip planner, keep only latitude and longitude in decimal
route_csv = pd.read_csv('./route.csv')

route2 = nav.Route()
for i in range(len(route_csv)):
    coordinate_x = route_csv.iloc[i,1]
    coordinate_y = route_csv.iloc[i,0]
    waypoint = nav.Waypoint(coordinate_x, coordinate_y)
    route2.append_waypoint(waypoint)

route2.plot_route()
    

print(route2)

route2.plot_route()
plt.show()
# %%
