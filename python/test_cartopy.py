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


text_shift = 0.0005
markersize = 30

church = marker.PlotMark(-3.33851, 47.72356, markersize,'church')
church.plot_land_mark()
light = marker.PlotMark(-3.36444, 47.72712, markersize,'lighthouse','Keroman')
light.plot_land_mark('magenta')
light.plot_text(text_shift)
light = marker.PlotMark(-3.36685, 47.72672, markersize, 'major_lighthouse')
light.plot_land_mark('red')
light = marker.PlotMark(-3.36752, 47.72670, markersize, 'major_lighthouse')
light.plot_land_mark('green')
light = marker.PlotMark(-3.37188, 47.71705, markersize, 'major_lighthouse')
light.plot_land_mark('red')

tower = marker.PlotMark(-3.36032, 47.72448, markersize,'tower')
tower.plot_land_mark()
tower.mark_type = 'major_lighthouse'
tower.plot_land_mark()
tower.plot_light_mark('green')
tower = marker.PlotMark(-3.35917, 47.72771, markersize,'tower')
tower.plot_land_mark()
tower.mark_type = 'major_lighthouse'
tower.plot_land_mark('green')

green = marker.PlotMark(-3.35197, 47.72534, markersize, 'spar')
green.plot_sea_mark('green', show_top_mark=False)
green.plot_light_mark('green')
green = marker.PlotMark(-3.35808, 47.71756, markersize, 'conical','M1')
green.plot_sea_mark('green', floating=True)
green.plot_text(text_shift)
green = marker.PlotMark(-3.35606, 47.71966, markersize, 'conical','M3')
green.plot_sea_mark('green', floating=True)
green.plot_text(text_shift)
green = marker.PlotMark(-3.36379, 47.72029, markersize, 'conical','N°3')
green.plot_sea_mark('green', floating=True)
green.plot_text(text_shift)
green = marker.PlotMark(-3.36396, 47.72219, markersize, 'pillar','Banc du Turc')
green.plot_sea_mark('green', floating=True)
green.plot_text(text_shift)
green.plot_light_mark('green')
green = marker.PlotMark(-3.36473, 47.72678, markersize, 'conical')
green.plot_sea_mark('green', show_top_mark=False, floating=True)
green = marker.PlotMark(-3.35857, 47.72813, markersize, 'spar','No7')
green.plot_sea_mark('green')
green.plot_light_mark('green')


red = marker.PlotMark(-3.35152, 47.72559, markersize, 'spar')
red.plot_sea_mark('red', show_top_mark=False)
red.plot_light_mark('red')
red2 = marker.PlotMark(-3.36533, 47.7162, markersize, 'spar', 'N°2')
red2.plot_sea_mark('red', floating = True)
red2.plot_light_mark('red')
red2.plot_text(text_shift)
red3 = marker.PlotMark(-3.35763, 47.71972, markersize,'can','M2')
red3.plot_sea_mark('red', floating=True)
red3.plot_text(text_shift)
red3 = marker.PlotMark(-3.35496, 47.72264, markersize,'can','M4')
red3.plot_sea_mark('red',show_top_mark=False, floating=True)
red3.plot_text(text_shift)
red4 = marker.PlotMark(-3.36723, 47.72172, markersize,'can','N°6')
red4.plot_sea_mark('red', show_top_mark=False, floating=True)
red4.plot_text(text_shift)
red4 = marker.PlotMark(-3.35353, 47.72723, markersize,'can','M6')
red4.plot_sea_mark('red', show_top_mark=False, floating=True)
red4.plot_text(text_shift)


south = marker.PlotMark(-3.3665, 47.71862, markersize, 'spar')
south.plot_sea_mark('south')
south.plot_light_mark('yellow')
south2 = marker.PlotMark(-3.36297, 47.7187, markersize, 'spar')
south2.plot_sea_mark('south', floating=True)



east = marker.PlotMark(-3.3703, 47.72651, markersize, 'spar')
east.plot_sea_mark('east', show_top_mark=False)

wreck = marker.PlotMark(-3.36989, 47.72604, markersize,'wreck_depth')
wreck.plot_danger_mark()
wreck2 = marker.PlotMark(-3.36894, 47.72544, markersize,'wreck_depth')
wreck2.plot_danger_mark()
wreck3 = marker.PlotMark(-3.35034, 47.728, markersize,'wreck')
wreck3.plot_danger_mark()
wreck3 = marker.PlotMark(-3.34759, 47.7275, markersize,'wreck')
wreck3.plot_danger_mark()
wreck4 = marker.PlotMark(-3.3578, 47.72015, markersize,'wreck')
wreck4.plot_danger_mark()
wreck5 = marker.PlotMark(-3.35807, 47.72099, markersize,'wreck')
wreck5.plot_danger_mark()


plt.show()



# %%
