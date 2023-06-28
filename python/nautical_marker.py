# %%
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.transforms as transforms

TOPMARKS_LIST =['green','red','north','south','east','west','danger','special','safe_Water']
LANDMARKS_LIST = ['lighthouse','major_lighthouse', 'tower', 'water_tower', 'church']
DANGERS_LIST = ['wreck', 'wreck_depth', 'danger','rock_covers','rock_depth']

class PlotMark:
    """ Plot mark """
    
    
    def __init__(self, position_x, position_y, markersize, mark_type, light_color=None, name = None ):
        text_shift = 0.0002
        self.position_x = position_x
        self.position_y = position_y
        self.markersize = markersize
        self.mark_type = mark_type
        self.name = name
        self.ligh_color = light_color
        if self.mark_type in DANGERS_LIST:
            self.plot_danger_mark()
        if self.mark_type in LANDMARKS_LIST:
            self.plot_land_mark()
        if light_color is not None:
            self.plot_light_mark(light_color)
        if self.name is not None:
            plt.text(self.position_x + text_shift, self.position_y + text_shift, self.name)    


    def plot_light_mark(self, color, angle = None):
        """ Plot light mark """
        if angle is None:
            angle = -0.45
        marker = build_light_path(angle)
        plt.plot(self.position_x, self.position_y, marker=marker, linestyle= None, 
                 markeredgecolor=color,
                markerfacecolor=color, markersize=self.markersize)

    def plot_danger_mark(self):
        """ plot danger marks """
        markersize = self.markersize/2
        
        if self.mark_type.lower() == 'danger':
            facecolor ='skyblue'
        else:
            facecolor='k'
        match self.mark_type.lower():
            case 'wreck':
                marker = build_wreck_path()
            case 'wreck_depth':
                marker = build_wreck_depth_path()
            case 'danger':
                marker = Path.unit_circle()
            case 'rock_covers':
                # plt.plot(position_x, position_y,'xk', markersize=markersize,)
                marker = (8,2,0.5)
            case 'rock_depth':
                marker = '+'
            case _:
                print('not defined danger')
        plt.plot(self.position_x, self.position_y, marker=marker, linestyle='solid',
            markerfacecolor=facecolor, markeredgecolor='k',
            markeredgewidth=0.5,
            markersize=markersize, label=type)
        if self.mark_type.lower() == 'wreck':
            plot_circle_line(self.position_x, self.position_y, 1.5 , 12)

    def plot_land_mark(self):
        """ plot land_marks """
        markersize = self.markersize
        match self.mark_type.lower():
            case 'lighthouse':
                marker = Path.unit_regular_star(5,0.3)
                facecolor='k'
                markersize = markersize/4
            case 'major_lighthouse':
                marker = Path.unit_regular_star(5,0.3)
                facecolor='k'
                markersize = markersize/3
            case 'tower':
                marker = build_land_tower_path(10,3)
                facecolor='none'
            case 'water_tower':
                marker = build_water_tower_path(10,3)
                facecolor='none'
            case 'church':
                marker = build_church_path()
                facecolor ='k'
                markersize = markersize/4
            case _:
                print('not defined landmark!')
        plt.plot(self.position_x, self.position_y, marker=marker, linestyle='solid',
                markerfacecolor=facecolor, markeredgecolor='k',
                markersize=markersize, label=type)
        if self.mark_type.lower() == 'major_lighthouse':
            plt.plot(self.position_x, self.position_y, marker='o', linestyle='solid',
                markerfacecolor=self.ligh_color, markeredgecolor=self.ligh_color,
                markersize=markersize/6, label=type)
            

    def plot_sea_mark(self, top_mark_type = None, show_top_mark = True, floating = False):
        """ plot nautical symbol """
        shape_height = 12
        topmark_size = 2
        color = select_color(top_mark_type)
        markersize = self.markersize
        width, shape_marker = select_shape(self.mark_type, shape_height)
        if show_top_mark is not True:
            symbol_marker = shape_marker
            markersize = markersize/2
        else:
            topmark_marker = select_topmark_marker(top_mark_type, topmark_size, shift_up=shape_height + 2)
            symbol_marker = Path.make_compound_path(shape_marker, topmark_marker)

        if floating:
            symbol_marker = symbol_marker.transformed(transforms.Affine2D().rotate(-0.3))

        plt.plot(self.position_x, self.position_y, marker=symbol_marker, linestyle='solid',
                markerfacecolor=color, markeredgecolor='k',markeredgewidth=0.5,
                markersize=markersize, label=top_mark_type)
        plot_circle_line(self.position_x, self.position_y, 1.5 , width + 2)

def select_color(top_mark_type):
    """ select color """
    match top_mark_type.lower():
        case 'green':
            color = 'green'
        case 'red' :
            color = 'red'
        case 'special':
            color ='yellow'
        case 'safe_water':
            color ='red'
        case _:
            color = 'black'
    return color

def select_shape(shape_type, shape_height):
    """ select shape """
    match shape_type.lower():
        case 'spar':
            width = 2
            shape_marker = build_rectangle_path(shape_height, width, 0)
        case 'can':
            width = 10
            shape_marker = build_rectangle_path(shape_height, width,0)
        case 'spherical':
            width = 10
            shape_marker = build_spherical(width*3/4)
        case 'conical':
            width = 10
            shape_marker = build_conical_path(shape_height, width)
        case 'pillar':
            width = 10
            shape_marker = build_pillar_path(shape_height, width)
        case 'tower':
            width = 10
            shape_marker = build_tower_path(shape_height,width)
        case _:
            print('not defined shape')
    return width, shape_marker

def select_topmark_marker(top_mark_type, size, shift_up):
    """ select topmark marker """
    match top_mark_type.lower():
        case 'green':
            topmark_marker = green_topmark(size, shift_up)
        case 'red':
            topmark_marker = red_topmark(height=size*2, width=size*2, shift_up=shift_up)
        case 'south':
            topmark_marker = south_topmark(size, shift_up)
        case 'north':
            topmark_marker = north_topmark(size, shift_up)
        case 'east':
            topmark_marker = east_topmark(size, shift_up)
        case 'west':
            topmark_marker = west_topmark(size, shift_up)
        case 'danger':
            topmark_marker = danger_topmark(size, shift_up)
        case 'special':
            topmark_marker = build_cross_path(shift_up + size, size)
        case 'safe_water':
            topmark_marker = build_circle_path(size, shift_up + size)
        case _:
            print(' Not a valid topmark')
    return topmark_marker

def build_triangle_path(size, shift_up):
    """ Build a triangle path """
    vertices = [(-size, shift_up), (0, shift_up + 2*size), (size, shift_up), (-size, shift_up)]
    codes = [1, 2, 2, 79]
    triangle_path = Path(vertices,codes)
    return triangle_path 

def build_triangle_down_path(size, shift_up):
    """ Build a triangle path """
    vertices = [(0, shift_up), (-size, shift_up + 2*size), (size, shift_up + 2*size), (0, shift_up)]
    codes = [1, 2, 2, 79]
    triangle_path = Path(vertices,codes)
    return triangle_path 

def build_rectangle_path(height, width, shift_up):
    """ Build a rectangle path """
    vertices = [(-width/2, shift_up), (-width/2, height + shift_up), 
                (width/2, height + shift_up), (width/2, shift_up), (-width/2, shift_up)]
    codes = [1, 2, 2, 2, 79]
    rectangle_path = Path(vertices,codes)
    return rectangle_path

def build_conical_path(height, width):
    """ Buils conocal path"""
    vertices =[(-width/2,0), (-width/2, height/3), (0,height), (width/2, height/3), (width/2,0),(-width/2,0)]
    codes = [1,3,2,3,2,79]
    conical_path = Path(vertices,codes)
    return conical_path

def build_pillar_path(height, width):
    """ Buils pillar path"""
    vertices =[(-width/2,0), (-width/4, height/3), (0,height), (width/4, height/3), (width/2,0),(-width/2,0)]
    codes = [1,2,2,2,2,79]
    pillar_path = Path(vertices,codes)
    return pillar_path

def build_cross_path(height, width):
    """ Build cross path """
    vertices = [(width/3*0, width/3*1 + height), (width/3*2, width/3*3 + height), (width/3*3, width/3*2 + height),
        (width/3*1, width/3*0 + height), (width/3*3, width/3*-2 + height), (width/3*2, width/3*-3 + height),
        (width/3*0, width/3*-1 + height), (width/3*-2, width/3*-3 + height), (width/3*-3, width/3*-2 + height),
        (width/3*-1, width/3*0 + height), (width/3*-3, width/3*2 + height), (width/3*-2, width/3*3 + height), (width/3*0, width/3*1 + height)]
    codes = [1,2,2,2,2,2,2,2,2,2,2,2,79]
    cross_path = Path(vertices, codes)
    return cross_path

def build_tower_path(height, width):
    """ build tower path """
    vertices = [(-width/2, 0), (-width/4, height), (width/4, height), (width/2,0), (-width/2,0)]
    codes = [1, 2, 2, 2, 79]
    tower_path = Path(vertices, codes)
    return tower_path

def build_church_path():
    """ Build church path """
    vertices = [(0,0), (0,2), (-1,3), (1,3), (0,2), (0,0), (2,0), (3,1), (3,-1), (2,0),
        (0,0), (0,-2), (1,-3), (-1,-3), (0,-2), (0,0), (-2,0), (-3,-1), (-3,1), (-2,0), (0,0)]
    codes=[1,3,2,2,3, 2,3,2,2,3, 2,3,2,2,3, 2,3,2,2,3, 79]
    church_path = Path(vertices, codes)
    return church_path

def build_land_tower_path(height, width):
    """ build tower path """
    botton_tower_path = build_tower_path(height*3/4,width)
    top_tower_path = build_rectangle_path(height/8,width/2,height*3/4)
    land_tower_path = Path.make_compound_path(botton_tower_path, top_tower_path)
    return land_tower_path

def build_water_tower_path(height, width):
    """ build tower path """
    botton_tower_path = build_tower_path(height*3/4,width)
    top_tower_path = build_rectangle_path(height/8,width,height*3/4)
    land_tower_path = Path.make_compound_path(botton_tower_path, top_tower_path)
    return land_tower_path

def build_wreck_path():
    """ build wreck path"""
    vertices =[(-2,0), (-3,2), (3,0), (-2,0)]
    codes = [1,2,2,79]
    boat_path = Path(vertices, codes)
    mast_path = Path([(0,0), (1,3)], [1,2])
    wreck_path = Path.make_compound_path(boat_path, mast_path)
    return wreck_path

def build_wreck_depth_path():
    """ build wreck path"""
    vertices =[(-2,0), (2,0), (0,1), (0,-1), (-1,0.5), (-1,-0.5), (1,0.5), (1,-0.5)]
    codes = [1,2,1,2,1,2,1,2]
    wreck_depth_path = Path(vertices, codes)
    return wreck_depth_path


def build_light_path(angle):
    """ build light path """
    vertices = [(1,0), (6,1), (6.5, 0.9), (6.8,0.7), (7,0), (6.8,-0.7 ), (6.5, -0.9), (6,-1),(6,0)]
    codes = [1,2,3,3,2,3,3,2,79]
    light_path = Path(vertices,codes)
    light_path = light_path.transformed(transforms.Affine2D().rotate(angle))
    return light_path

def build_spherical(width):
    """ Build spherical path"""
    tmp = Path.arc(-30,210)
    vertices = tmp.vertices*width
    for vertice in vertices:
        vertice[1]=vertice[1]+width/2
    codes = tmp.codes
    spherical_path = Path(vertices, codes)  
    return spherical_path


def build_line_path(start, stop):
    """ Build line path """
    vertices =[(0,start), (0,stop)]
    codes = [1,2]
    line_path = Path(vertices,codes)
    return line_path

def build_h_line_path(start, stop):
    """ Build horizontal line path """
    vertices =[(start,0), (stop,0)]
    codes = [1,2]
    line_path = Path(vertices,codes)
    return line_path

def build_circle_path(size, shift_up):
    """ Build circle path """
    circle = Path.circle([0.0, shift_up], size)
    return circle

def plot_circle_line(position_x, position_y,circle_size, line_size):
    """ Build point path """
    line_path1 = build_h_line_path(-line_size, -circle_size)
    circle_path = build_circle_path(circle_size,0)
    line_path2 = build_h_line_path(line_size, circle_size)
    marker = Path.make_compound_path(line_path1, circle_path, line_path2)
    plt.plot(position_x, position_y, marker=marker, linestyle='solid',
            markerfacecolor='white', markeredgecolor='k',
            markeredgewidth=0.2,
            markersize=line_size*2, label='Green Beacon')

def green_topmark(size, shift_up):
    """ plot green beacon """
    triangle_marker = build_triangle_path(size,shift_up)
    return triangle_marker

def red_topmark(height, width, shift_up):
    """ Plot red beacon """
    red_marker = build_rectangle_path(height,width,shift_up)
    return red_marker

def north_topmark(size, shift_up):
    """ Plot north beacon """
    triangle_marker1 = build_triangle_path(size, shift_up)
    triangle_marker2 = build_triangle_path(size, shift_up + 2*size + 2)
    north_marker = Path.make_compound_path(triangle_marker1, triangle_marker2)
    return north_marker

def south_topmark(size, shift_up):
    """ Plot north beacon """
    triangle_marker1 = build_triangle_down_path(size, shift_up)
    triangle_marker2 = build_triangle_down_path(size, shift_up + 2*size + 2)
    south_marker = Path.make_compound_path(triangle_marker1, triangle_marker2)
    return south_marker

def east_topmark(size, shift_up):
    """ Plot east beacon """
    triangle_marker1 = build_triangle_down_path(size, shift_up)
    triangle_marker2 = build_triangle_path(size, shift_up + 2*size + 2)
    east_marker = Path.make_compound_path(triangle_marker1, triangle_marker2)
    return east_marker

def west_topmark(size, shift_up):
    """ Plot west beacon """
    triangle_marker1 = build_triangle_path(size, shift_up)
    triangle_marker2 = build_triangle_down_path(size, shift_up + 2*size + 2)
    west_marker = Path.make_compound_path(triangle_marker1, triangle_marker2)
    return west_marker

def danger_topmark(size, shift_up):
    """ Plot danger beacon """
    circle_marker1 = build_circle_path(size, shift_up + size)
    circle_marker2 = build_circle_path(size, shift_up + 3*size + 2)
    danger_marker = Path.make_compound_path(circle_marker1, circle_marker2)
    return danger_marker

if __name__ == "__main__":

    
    shape_type_list =['conical','can','spherical','spar','pillar','tower']
    markersize=40

    plt.figure(1)
    for j, shape in enumerate(shape_type_list):
        plt.text(1,j*2,shape.capitalize(), horizontalalignment='center')

    for i, topmark in enumerate(TOPMARKS_LIST):
        plt.text(i+2,len(shape_type_list)*2, topmark.capitalize(), horizontalalignment='center')
        for j, shape in enumerate(shape_type_list):
            sea_mark = PlotMark(i+2, j*2, markersize,shape)
            sea_mark.plot_sea_mark(top_mark_type=topmark, floating=False)
    plt.title('Sea marks as a function of shape and topmark')
    plot_circle_line(1, 13, 2, 4)
    plt.axis('off')
    #plt.show(block="True")
    plt.draw()

    plt.figure(2)
    markersize = 50
    

    plt.text(1,15,'Land marks')
    for i, mark in enumerate(LANDMARKS_LIST):
        plt.text(i*2+4,17,mark.capitalize(), horizontalalignment='center')
        land_mark = PlotMark(i*2+4, 15, markersize, mark)
    
    plt.text(1,19,'Danger marks')
    for i, mark in enumerate(DANGERS_LIST):
        plt.text(i*2+4,21,mark.capitalize(), horizontalalignment='center')
        danger_mark = PlotMark(i*2+4,19, markersize,mark)
    plt.text(1,23,'Light')
    
    
    light1 = PlotMark(3,23, markersize,'Spar',light_color='yellow')
    light1.plot_sea_mark('East',floating=True)
    
    light2 = PlotMark(5,23, markersize,'Can', light_color='green')
    light2.plot_sea_mark('Green', floating=False)
    
    light3 = PlotMark(7,23,markersize,'Lighthouse',light_color='red')
   
    
    plot_circle_line(1, 25, 2, 4)
    

    plt.axis('off')
    plt.title('Nautical symbols')
    plt.show()
