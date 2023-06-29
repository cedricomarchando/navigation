# %%
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import nautical_marker as marker



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

marker.PlotMark(-3.33851, 47.72356,'church')
marker.PlotMark(-3.36444, 47.72712,'lighthouse', None, 'magenta','Keroman')
marker.PlotMark(-3.36685, 47.72672, 'major_lighthouse', None, 'red')
marker.PlotMark(-3.36752, 47.72670, 'major_lighthouse', None, 'green')
marker.PlotMark(-3.37188, 47.71705, 'major_lighthouse', None,'red')
marker.PlotMark(-3.36705, 47.72751, 'lighthouse', None, 'red')
marker.PlotMark(-3.36774, 47.72757, 'lighthouse', None, 'green')
marker.PlotMark(-3.37408, 47.71497, 'lighthouse', None, 'red')

marker.PlotMark(-3.36032, 47.72448, 'land_tower')
marker.PlotMark(-3.36032, 47.72448, 'major_lighthouse',None, 'green')
marker.PlotMark(-3.35917, 47.72712, 'land_tower')
marker.PlotMark(-3.35917, 47.72712, 'major_lighthouse',None, 'green')
marker.PlotMark(-3.35995, 47.72535,'land_tower',None, None, 'Tourelle Aimé')

marker.PlotMark(-3.35197, 47.72534, 'spar', 'green', 'green', show_top_mark=False)
marker.PlotMark(-3.35808, 47.71756, 'conical', 'green',  None, 'M1', floating=True)
marker.PlotMark(-3.35606, 47.71966, 'conical', 'green',  None, 'M3', floating=True)
marker.PlotMark(-3.36379, 47.72029, 'conical', 'green',  None,'N°3', floating=True)
marker.PlotMark(-3.36396, 47.72219, 'pillar', 'green',  'green', 'Banc du Turc', floating=True)
marker.PlotMark(-3.36473, 47.72678, 'conical','green', show_top_mark=False, floating=True)
marker.PlotMark(-3.35857, 47.72813, 'spar', 'green',  'green','No7')
marker.PlotMark(-3.36118, 47.72575, 'conical', 'green',  'green', 'N°5', floating=True)
marker.PlotMark(-3.35366, 47.72457, 'conical','green',  None, 'M5', floating=True)
marker.PlotMark(-3.35920, 47.72785, 'conical', 'green',  'green', 'N°7', floating=True)
marker.PlotMark(-3.36393, 47.71349, 'conical', 'green',  None, 'N°1', floating=True)
marker.PlotMark(-3.35369, 47.73134, 'tower', 'green', 'green',  'Pengarne', show_top_mark=False)
marker.PlotMark(-3.35258, 47.73248, 'conical','green', 'green', 'No9', floating=True)
marker.PlotMark(-3.3575, 47.71276, 'spar', 'green','green' )

marker.PlotMark(-3.35152, 47.72559, 'spar', 'red', 'red', None, show_top_mark=False)
marker.PlotMark(-3.36533, 47.7162, 'spar', 'red', 'red', 'N°2', floating = True)
marker.PlotMark(-3.35763, 47.71972,'can', 'red', None, 'M2', floating=True)
marker.PlotMark(-3.35496, 47.72264,'can', 'red', None, 'M4', show_top_mark=False, floating=True)
marker.PlotMark(-3.36723, 47.72172,'can', 'red', None, 'N°6', show_top_mark=False, floating=True)
marker.PlotMark(-3.35353, 47.72723,'can', 'red', None, 'M6', show_top_mark=False, floating=True)
marker.PlotMark(-3.36601, 47.71843,'can', 'red', None, 'N°4', show_top_mark=False, floating=True)
marker.PlotMark(-3.36722, 47.71793,'spar', 'red' )
marker.PlotMark(-3.36667, 47.71339,'tower', 'red_bis', 'red', 'Le Cochon', show_top_mark=False)
marker.PlotMark(-3.36741, 47.71362,'spar', 'red')
marker.PlotMark(-3.36785, 47.71330,'spar', 'red')
marker.PlotMark(-3.35898, 47.71376,'can', 'red', floating=True)

marker.PlotMark(-3.3665, 47.71862, 'spar', 'south','yellow')
marker.PlotMark(-3.36297, 47.7187, 'spar', 'south', floating=True)
marker.PlotMark(-3.3703, 47.72651, 'spar', 'east', show_top_mark=False)
marker.PlotMark(-3.35252, 47.73136, 'spar', 'east')

marker.PlotMark(-3.36108, 47.71447, 'spar', 'west', floating=True)
marker.PlotMark(-3.35545, 47.7302, 'spar','north', 'yellow', floating=True)
marker.PlotMark(-3.3546, 47.73007, 'spar','north','yellow', floating=True)

marker.PlotMark(-3.36989, 47.72604,'wreck_depth')
marker.PlotMark(-3.36894, 47.72544,'wreck_depth')
marker.PlotMark(-3.35034, 47.728,'wreck')
marker.PlotMark(-3.34759, 47.7275,'wreck')
marker.PlotMark(-3.3578, 47.72015,'wreck')
marker.PlotMark(-3.35807, 47.72099,'wreck')
marker.PlotMark(-3.35662, 47.72181,'wreck')
marker.PlotMark(-3.34620, 47.72670,'wreck')
marker.PlotMark(-3.34620, 47.72670,'wreck')
marker.PlotMark(-3.34673, 47.72586,'wreck')
marker.PlotMark(-3.37243, 47.71915,'wreck')
marker.PlotMark(-3.36691, 47.71489,'danger')
marker.PlotMark(-3.36691, 47.71489,'wreck_depth')
marker.PlotMark(-3.35249, 47.71428,'wreck')
marker.PlotMark(-3.35214, 47.71411,'wreck')
marker.PlotMark(-3.35214, 47.71398,'wreck')
marker.PlotMark(-3.35227, 47.71316,'wreck')

plt.show()



# %%
