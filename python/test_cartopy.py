# %%
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import nautical_marker as marker



# rade.png obtained from OpenSeaMap
#img = plt.imread("../map/rade.png")
img = plt.imread('rade.png')

img_extent = (-3.3782, -3.33217, 47.715, 47.7309)

ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent( [-3.3782, -3.33217, 47.715, 47.7309], crs=ccrs.PlateCarree())


plt.imshow(img, origin='upper', extent=img_extent, transform=ccrs.PlateCarree())
#plt.figure(figsize=(10, 5))

marker.PlotMark.markersize=30

marker.PlotMark(-3.33851, 47.72356,'church')
marker.PlotMark(-3.36444, 47.72712,'lighthouse', 'magenta','Keroman')
marker.PlotMark(-3.36685, 47.72672, 'major_lighthouse', 'red')
marker.PlotMark(-3.36752, 47.72670, 'major_lighthouse', 'green')
marker.PlotMark(-3.37188, 47.71705, 'major_lighthouse', 'red')
marker.PlotMark(-3.36705, 47.72751, 'lighthouse', 'red')
marker.PlotMark(-3.36774, 47.72757, 'lighthouse', 'green')


tower = marker.PlotMark(-3.36032, 47.72448, 'tower', 'green')
tower.mark_type = 'major_lighthouse'
tower.plot_land_mark()
tower = marker.PlotMark(-3.35917, 47.72712, 'tower', 'green')
tower.mark_type = 'major_lighthouse'
tower.plot_land_mark()
tower2 = marker.PlotMark(-3.35995, 47.72535,'tower', None, 'Tourelle Aimé')

green = marker.PlotMark(-3.35197, 47.72534, 'spar','green')
green.plot_sea_mark('green', show_top_mark=False)
green = marker.PlotMark(-3.35808, 47.71756, 'conical', None, 'M1')
green.plot_sea_mark('green', floating=True)
green = marker.PlotMark(-3.35606, 47.71966, 'conical', None, 'M3')
green.plot_sea_mark('green', floating=True)
green = marker.PlotMark(-3.36379, 47.72029, 'conical', None,'N°3')
green.plot_sea_mark('green', floating=True)
green = marker.PlotMark(-3.36396, 47.72219, 'pillar', 'green', 'Banc du Turc')
green.plot_sea_mark('green', floating=True)
green = marker.PlotMark(-3.36473, 47.72678, 'conical')
green.plot_sea_mark('green', show_top_mark=False, floating=True)
green = marker.PlotMark(-3.35857, 47.72813, 'spar', 'green','No7')
green.plot_sea_mark('green')
green = marker.PlotMark(-3.36118, 47.72575, 'conical', 'green', 'N°5')
green.plot_sea_mark('green', floating=True)
green = marker.PlotMark(-3.35366, 47.72457, 'conical', None, 'M5')
green.plot_sea_mark('green', floating=True)
green = marker.PlotMark(-3.35920, 47.72785, 'conical', 'green', 'N°7')
green.plot_sea_mark('green', floating=True)


red = marker.PlotMark(-3.35152, 47.72559, 'spar', 'red', None )
red.plot_sea_mark('red', show_top_mark=False)
red2 = marker.PlotMark(-3.36533, 47.7162, 'spar', 'red', 'N°2')
red2.plot_sea_mark('red', floating = True)
red3 = marker.PlotMark(-3.35763, 47.71972,'can', None, 'M2')
red3.plot_sea_mark('red', floating=True)
red3 = marker.PlotMark(-3.35496, 47.72264,'can', None, 'M4')
red3.plot_sea_mark('red',show_top_mark=False, floating=True)
red4 = marker.PlotMark(-3.36723, 47.72172,'can', None, 'N°6')
red4.plot_sea_mark('red', show_top_mark=False, floating=True)
red4 = marker.PlotMark(-3.35353, 47.72723,'can', None, 'M6')
red4.plot_sea_mark('red', show_top_mark=False, floating=True)
red4 = marker.PlotMark(-3.36601, 47.71843,'can', None, 'N°4')
red4.plot_sea_mark('red', show_top_mark=False, floating=True)
red4 = marker.PlotMark(-3.36722, 47.71793,'spar')
red4.plot_sea_mark('red')


south = marker.PlotMark(-3.3665, 47.71862, 'spar','yellow')
south.plot_sea_mark('south')
south2 = marker.PlotMark(-3.36297, 47.7187, 'spar')
south2.plot_sea_mark('south', floating=True)



east = marker.PlotMark(-3.3703, 47.72651, 'spar')
east.plot_sea_mark('east', show_top_mark=False)

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

    
plt.show()



# %%
