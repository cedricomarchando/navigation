# %%
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import nautical_marker as marker
import pandas as pd
import numpy as np



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

marker.PlotMark.markersize=30

# %%

marks_df = pd.read_csv('marks.csv')
marks_df = marks_df.replace('None',None)
marks_df = marks_df.replace(np.nan,None)


# %%

for i in range(len(marks_df)):
    mark_data = marks_df.loc[i]
    marker.PlotMark(float(mark_data[0]),float(mark_data[1]), mark_data[2], mark_data[3],
                    mark_data[4], mark_data[5], mark_data[6], mark_data[7])
    

plt.show()
# %%
