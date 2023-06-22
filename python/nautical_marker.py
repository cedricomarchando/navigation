# %%
import matplotlib.pyplot as plt
from matplotlib.path import Path


def plot_nautical_symbol(position_x, position_y, shape_type, top_mark_type):
    """ plot nautical symbol """
    
    shape_height = 12
    topmark_size = 2
    color = select_color(top_mark_type)
    
    shape_marker = select_shape(shape_type, shape_height)
    topmark_marker = select_topmark_marker(top_mark_type, topmark_size, shift_up=shape_height + 2)
    symbol_marker = Path.make_compound_path(shape_marker, topmark_marker)
    
    plt.plot(position_x, position_y, marker=symbol_marker, linestyle='solid',
            markerfacecolor=color, markeredgecolor='k',
            markersize=50, label=top_mark_type)
    plot_circle_line(position_x, position_y, 1.5 , 4)
    


def select_color(top_mark_type):
    """ select color """
    match top_mark_type:
        case 'green':
            color = 'green'
        case 'red':
            color = 'red'
        case _:
            color = 'black'
    return color

def select_shape(shape_type, shape_height):
    """ select shape """
    match shape_type:
        case 'spar':
            shape_marker = build_rectangle_path(shape_height,2,0)
        case 'can':
            shape_marker = build_rectangle_path(shape_height,10,0)
        case 'conical':
            shape_marker = build_conical_path(shape_height,10)
        case _:
            print('not defined shape')
    return shape_marker

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

def build_conical_path(height,width):
    """ Buils conocal path"""
    vertices =[(-width/2,0), (-width/2, height/3), (0,height), (width/2, height/3), (width/2,0),(-width/2,0),   ]
    codes = [1,3,2,3,2,79]
    conical_path = Path(vertices,codes)
    return conical_path

def build_line_path(start,stop):
    """ Build line path """
    vertices =[(0,start),(0,stop)]
    codes = [1,2]
    line_path = Path(vertices,codes)
    return line_path

def build_h_line_path(start,stop):
    """ Build horizontal line path """
    vertices =[(start,0),(stop,0)]
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
            markerfacecolor='None', markeredgecolor='k',
            markersize=10, label='Green Beacon')
    
    
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
    
    topmark_type_list =['green','red','north','south','east','west','danger']
    shape_type_list =['conical','can','spar']
    
    
    for i, topmark in enumerate(topmark_type_list):
        for j, shape in enumerate(shape_type_list):
            plot_nautical_symbol(i, j*2, shape_type=shape, top_mark_type=topmark)

    plot_circle_line(i+1, 10, 2, 4)
    plt.show()