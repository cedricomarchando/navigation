# %%
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.transforms as transforms

def plot_land_marks(position_x, position_y, markersize, type):
    """ plot land_marks"""
    match type:
        case 'lighthouse':
            marker = Path.unit_regular_star(5,0.5)
            facecolor='k'
        case 'tower':
            marker = build_land_tower_path(10,2)
            facecolor='none'
        case 'water_tower':
            marker = build_water_tower_path(10,2)
            facecolor='none'
        case _:
            print('notdefined landmark')
            
    plt.plot(position_x, position_y, marker=marker, linestyle='solid',
            markerfacecolor=facecolor, markeredgecolor='k',
            markersize=markersize, label=type)
    

def plot_sea_marks(position_x, position_y, markersize, shape_type, top_mark_type, floating):
    """ plot nautical symbol """
    
    shape_height = 12
    topmark_size = 2
    color = select_color(top_mark_type)
    
    width, shape_marker = select_shape(shape_type, shape_height)
    if (top_mark_type  == 'green_no_top') or (top_mark_type  == 'red_no_top'):
        symbol_marker = shape_marker
        markersize = markersize/2
    else:
        topmark_marker = select_topmark_marker(top_mark_type, topmark_size, shift_up=shape_height + 2)
        symbol_marker = Path.make_compound_path(shape_marker, topmark_marker)
    
    if floating:
        symbol_marker = symbol_marker.transformed(transforms.Affine2D().rotate(-0.3))

    plt.plot(position_x, position_y, marker=symbol_marker, linestyle='solid',
            markerfacecolor=color, markeredgecolor='k',
            markersize=markersize, label=top_mark_type)
    plot_circle_line(position_x, position_y, 1.5 , width + 2)
    


def select_color(top_mark_type):
    """ select color """
    match top_mark_type:
        case 'green':
            color = 'green'
        case 'green_no_top':
            color = 'green'
        case 'red' :
            color = 'red'
        case 'red_no_top' :
            color = 'red'
        case 'special':
            color ='yellow'
        case _:
            color = 'black'
    return color

def select_shape(shape_type, shape_height):
    """ select shape """
    match shape_type:
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
    match top_mark_type:
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
    vertices =[(-width/2,0), (-width/2, height/3), (0,height), (width/2, height/3), (width/2,0),(-width/2,0),   ]
    codes = [1,3,2,3,2,79]
    conical_path = Path(vertices,codes)
    return conical_path

def build_pillar_path(height, width):
    """ Buils pillar path"""
    vertices =[(-width/2,0), (-width/4, height/3), (0,height), (width/4, height/3), (width/2,0),(-width/2,0),   ]
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
    
    topmark_type_list =['green','red','north','south','east','west','danger','special','green_no_top','red_no_top']
    shape_type_list =['conical','can','spherical','spar','pillar','tower']
    MARKERSIZE=50
    
    plt.figure(1)
    for j, shape in enumerate(shape_type_list):
        plt.text(1,j*2,shape, horizontalalignment='center')
    
    for i, topmark in enumerate(topmark_type_list):
        plt.text(i+2,len(shape_type_list)*2, topmark, horizontalalignment='center')
        for j, shape in enumerate(shape_type_list):
            plot_sea_marks(i+2, j*2, MARKERSIZE, shape_type=shape, top_mark_type=topmark, floating=False)

    plot_circle_line(1, 16, 2, 4)
    plot_land_marks(1, 15, MARKERSIZE/4, 'lighthouse')
    plot_land_marks(2, 15, MARKERSIZE, 'tower')
    plot_land_marks(3, 15, MARKERSIZE, 'water_tower')
    
    plt.axis('off')
    plt.xlabel('topmark')
    plt.ylabel('shape')
    plt.title('Nautical fixed mark symbols')
    
    plt.show()
    """
    plt.figure(2)
    for j, shape in enumerate(shape_type_list):
        plt.text(1,j*2,shape, horizontalalignment='center')
    
    for i, topmark in enumerate(topmark_type_list):
        plt.text(i+2,len(shape_type_list)*2, topmark, horizontalalignment='center')
        for j, shape in enumerate(shape_type_list):
            plot_sea_marks(i+2, j*2, MARKERSIZE, shape_type=shape, top_mark_type=topmark, floating=True)

    plot_circle_line(1, 12, 2, 4)
    plt.axis('off')
    plt.xlabel('topmark')
    plt.ylabel('shape')
    plt.title('Nautical floating mark symbols')
    
    plt.show()
    """
    