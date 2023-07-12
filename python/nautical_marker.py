# %%
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.transforms as transforms
from enum import Enum, auto


LANDMARKS_SET : set[str] = {'lighthouse', 'major_lighthouse', 'light_tower', 'land_tower', 'water_tower', 'church'}
DANGERS_SET : set[str] = {'wreck', 'wreck_depth', 'danger','rock_covers','rock_depth'}
SEAMARK_SET : set[str] = {'conical','can','spherical','spar','pillar','tower'}

HARBOURS_SET : set[str] = {'marina','anchorage','no_anchorage', 'fish', 'no_fish', 'slipway', 'steps'}
TOPMARKS_SET : set[str] = {'green', 'green_bis', 'red', 'red_bis', 'north', 'south', 'east', 'west',
                'danger', 'special', 'safe_water', 'emergency'}

MARKS_LIST : set[str] = LANDMARKS_SET | DANGERS_SET | SEAMARK_SET | HARBOURS_SET

class TopMark(Enum):
    GREEN = auto()
    GREEN_BIS = auto()
    RED = auto()
    RED_BIS = auto()
    NORTH = auto()
    SOUTH = auto()
    EAST = auto()
    WEST = auto()
    DANGER = auto()
    SPECIAL = auto()
    SAFE_WATER = auto()
    EMERGENCY = auto()

class PlotMark:
    """ Plot mark """
    text_shift = 0.0002
    markersize = 30

    def __init__(self, position_x :float, position_y : float, mark_type : str, top_mark_type : str = None,
                 light_color:str=None, name:str=None, floating:bool = False, show_top_mark:bool = True):
        self.position_x = position_x
        self.position_y = position_y
        self.mark_type = mark_type.lower()
        self.top_mark_type = top_mark_type
        self.name = name
        self.light_color = light_color
        self.floating = floating
        self.show_top_mark = show_top_mark

        if self.top_mark_type is not None:
            self.top_mark_type = self.top_mark_type.lower()
            self.plot_sea_mark()
        if self.mark_type in DANGERS_SET:
            self.plot_danger_mark()
        if self.mark_type in LANDMARKS_SET:
            self.plot_land_mark()
        if self.mark_type in HARBOURS_SET:
            self.plot_harbour_mark()
        if light_color is not None:
            self.plot_light_mark(light_color)
        if self.name is not None:
            plt.text(self.position_x + self.text_shift, self.position_y + self.text_shift, self.name)


    def plot_light_mark(self, color : str, angle :float = None) -> None:
        """ Plot light mark """
        if angle is None:
            angle = -0.45
        marker = BuildPath.light(angle)
        plt.plot(self.position_x, self.position_y, marker=marker, linestyle= None, 
                 markeredgecolor=color,
                markerfacecolor=color, markersize=self.markersize)
        
    def plot_harbour_mark(self) -> None:
        """ Plot light mark """
        match self.mark_type:
            case 'marina':
                marker = BuildPath.marina()
            case 'anchorage':
                marker = BuildPath.anchorage()
            case 'no_anchorage':
                marker = BuildPath.no_anchorage()
            case 'fish':
                marker = BuildPath.fish()
            case 'no_fish':
                marker = BuildPath.no_fish()
            case 'slipway':
                marker = BuildPath.slipway()
            case 'steps':
                marker = BuildPath.steps()
            case _:
                print('not defined harbour')
        plt.plot(self.position_x, self.position_y, marker = marker, markersize = PlotMark.markersize/2,
            fillstyle='none', markeredgewidth=1, markeredgecolor='m')

    def plot_danger_mark(self) -> None:
        """ plot danger marks """
        marker_size = self.markersize/2
        
        if self.mark_type == 'danger':
            facecolor ='skyblue'
        else:
            facecolor='k'
        match self.mark_type:
            case 'wreck':
                marker = BuildPath.wreck()
            case 'wreck_depth':
                marker = BuildPath.wreck_depth()
            case 'danger':
                marker = Path.unit_circle()
            case 'rock_covers':
                # plt.plot(position_x, position_y,'xk', markersize=markersize,)
                marker = (8,2,0.5)
                marker_size = marker_size/2
            case 'rock_depth':
                marker = '+'
                marker_size = marker_size/2
            case _:
                print('not defined danger')
        plt.plot(self.position_x, self.position_y, marker=marker, linestyle='solid',
            markerfacecolor=facecolor, markeredgecolor='k',
            markeredgewidth=0.5,
            markersize=marker_size, label=type)
        if self.mark_type == 'wreck':
            self.plot_white_circle(10)

    def plot_land_mark(self) -> None:
        """ plot land_marks """
        markersize = self.markersize
        match self.mark_type:
            case 'lighthouse':
                marker = Path.unit_regular_star(5,0.3)
                facecolor='k'
                markersize = markersize/4
            case 'major_lighthouse':
                marker = Path.unit_regular_star(5,0.3)
                facecolor='k'
                markersize = markersize/3
            case 'light_tower':
                marker = BuildPath.land_tower(10,3)
                facecolor='none'
                self.plot_white_circle(10)
            case 'land_tower':
                marker = BuildPath.land_tower(10,3)
                facecolor='none'
                self.plot_white_circle(10)
            case 'water_tower':
                marker = BuildPath.water_tower(10,3)
                facecolor='none'
                self.plot_white_circle(10)
            case 'church':
                marker = BuildPath.church()
                facecolor ='k'
                markersize = markersize/4
            case _:
                print('not defined landmark!')
        plt.plot(self.position_x, self.position_y, marker=marker, linestyle='solid',
                markerfacecolor=facecolor, markeredgecolor='k',
                markersize=markersize, label=type)
        if self.mark_type == 'light_tower':
                markersize = markersize/3
                marker = Path.unit_regular_star(5,0.3)
                plt.plot(self.position_x, self.position_y, marker=marker, linestyle='solid',
                markerfacecolor='k', markeredgecolor='k',
                markersize=markersize, label=type)
        
        if self.mark_type == 'major_lighthouse' or self.mark_type == 'light_tower':
            plt.plot(self.position_x, self.position_y, marker='o', linestyle='solid',
                markerfacecolor=self.light_color, markeredgecolor=self.light_color,
                markersize=markersize/6, label=type)
            

    def plot_sea_mark(self) -> None:
        """ plot nautical symbol """
        shape_height = 12
        topmark_size = 2
        color, color2 = self.select_color()
        markersize = self.markersize
        shape_marker, shape_marker2 = self.select_shape(self.top_mark_type, shape_height)
        if self.show_top_mark is False:
            symbol_marker = shape_marker
            symbol_marker2 = shape_marker2
            markersize = 2*markersize/3
        else:
            topmark_marker = self.select_topmark_marker(topmark_size, shift_up=shape_height + topmark_size/2)
            symbol_marker = Path.make_compound_path(shape_marker, topmark_marker)
            symbol_marker2 = Path.make_compound_path(shape_marker2, topmark_marker)

        if self.floating:
            symbol_marker = symbol_marker.transformed(transforms.Affine2D().rotate(-0.3))
            symbol_marker2 = symbol_marker2.transformed(transforms.Affine2D().rotate(-0.3))

        if self.mark_type == 'spar':
            self.plot_ref_line(self.markersize/4)
        else:
            self.plot_ref_line(self.markersize/2)
        
        plt.plot(self.position_x, self.position_y, marker=symbol_marker, linestyle='solid',
                markerfacecolor=color,
                markeredgecolor='k',markeredgewidth=0.5,
                markersize=markersize)
        plt.plot(self.position_x, self.position_y, marker=symbol_marker2, linestyle='solid',
                markerfacecolor=color2,
                markeredgecolor='k',markeredgewidth=0.5,
                markersize=markersize)
        
        self.plot_white_circle(shape_height)
        
        
    def plot_ref_line(self,size) -> None:
        """ Build point path """
        marker = Path([(-1,0), (1,0)],[1,2])
        plt.plot(self.position_x, self.position_y, marker=marker, 
                markeredgecolor='k',
                markeredgewidth=0.5,
                markersize=size)
        
    def plot_white_circle(self, circle_size: float) -> None:
        """ plot white circle"""
        circle_path = BuildPath.circle(circle_size,0)
        plt.plot(self.position_x, self.position_y, marker=circle_path,
                markerfacecolor='white', markeredgecolor='k',
                markeredgewidth=0.2,
                markersize=self.markersize/12)

    def select_shape(self, top_mark_type: str, shape_height: float) -> tuple[Path, Path]:
        """ select shape """
        width = 10
        match self.mark_type:
            case 'spar':
                shape_marker = BuildPath.rectangle(shape_height, width/5, 0)
                match top_mark_type:
                    case 'green_bis' | 'red_bis' | 'danger' | 'east':
                        marker_tmp1 = BuildPath.rectangle(shape_height/3, width/5, 0)
                        marker_tmp2 = BuildPath.rectangle(shape_height/3, width/5, 2*shape_height/3)
                        shape_marker2 = Path.make_compound_path( marker_tmp1, marker_tmp2)
                    case 'north':
                        shape_marker2 = BuildPath.rectangle(shape_height/2, width/5, shape_height/2)
                    case 'south':
                        shape_marker2 = BuildPath.rectangle(shape_height/2, width/5, 0)   
                    case 'west':
                        shape_marker2 = BuildPath.rectangle(shape_height/3, width/5, shape_height/3)
                    case 'safe_water':
                        shape_marker2 = BuildPath.rectangle(shape_height, width/15, 0)
                    case 'emergency':
                        shape_marker2 = BuildPath.rectangle(shape_height, width/15, 0)
                    case _:
                        shape_marker2 = shape_marker
            case 'can':
                shape_marker = BuildPath.rectangle(shape_height, width,0)
                match top_mark_type:
                    case 'green_bis' | 'red_bis' | 'danger' | 'east':
                        marker_tmp1 = BuildPath.rectangle(shape_height/3, width, 0)
                        marker_tmp2 = BuildPath.rectangle(shape_height/3, width, 2*shape_height/3)
                        shape_marker2 = Path.make_compound_path( marker_tmp1, marker_tmp2)
                    case 'north':
                        shape_marker2 = BuildPath.rectangle(shape_height/2, width, shape_height/2)
                    case 'south':
                        shape_marker2 = BuildPath.rectangle(shape_height/2, width, 0)   
                    case 'west':
                        shape_marker2 = BuildPath.rectangle(shape_height/3, width, shape_height/3)
                    case 'safe_water':
                        shape_marker2 = BuildPath.rectangle(shape_height, width/3, 0)
                    case 'emergency':
                        shape_marker2 = BuildPath.rectangle(shape_height, width/3, 0)
                    case _:
                        shape_marker2 = shape_marker
            case 'spherical':
                shape_marker = BuildPath.spherical(width*3/4, -30, 210, width*3/8)
                match top_mark_type:
                    case 'green_bis' | 'red_bis' | 'danger' | 'east':
                        marker_tmp1 = BuildPath.spherical(width*3/4, 30, 150, width*3/8)
                        marker_tmp2 = BuildPath.tower(width/3, 5*width/8, width*3/4, 0)
                        shape_marker2 = Path.make_compound_path( marker_tmp1, marker_tmp2)
                    case 'north':
                        shape_marker2 = BuildPath.spherical(width*3/4, 0, 180, width*3/8)
                    case 'south':
                        shape_marker2 = BuildPath.tower(width/3, 5*width/8, width*3/4, 0)
                    case 'west':
                        shape_marker2 = BuildPath.tower(width/3, width*3/4, 2*width/3, width/3)
                    case 'safe_water':
                        shape_marker2 = BuildPath.triangle(width/2, shape_height, 0)
                    case 'emergency':
                        shape_marker2 = BuildPath.triangle(width/2, shape_height, 0)
                    case _:
                        shape_marker2 = shape_marker
            case 'conical':
                shape_marker = BuildPath.conical(shape_height, width)
                match top_mark_type:
                    case 'green_bis' | 'red_bis' | 'danger' | 'east':
                        marker_tmp1 = BuildPath.tower(shape_height/3, width/2, 3*width/8, 0)
                        marker_tmp2 = BuildPath.triangle(  width/2 ,shape_height/3, 2*shape_height/3)
                        shape_marker2 = Path.make_compound_path( marker_tmp1, marker_tmp2)
                    case 'north':
                        shape_marker2 = BuildPath.triangle(3*width/4, 2*shape_height/3, shape_height/3)
                    case 'south':
                        shape_marker2 = BuildPath.tower(shape_height/3, width/2, 3*width/8, 0)
                    case 'west':
                        shape_marker2 = BuildPath.tower(shape_height/3, 7*width/16, width/4, shape_height/4)
                    case 'safe_water':
                        shape_marker2 = BuildPath.triangle(shape_height/2, shape_height, 0)
                    case 'emergency':
                        shape_marker2 = BuildPath.triangle(shape_height/2, shape_height, 0)
                    case _:
                        shape_marker2 = shape_marker
                
            case 'pillar':
                shape_marker = BuildPath.pillar(shape_height, width)
                match top_mark_type:
                    case 'green_bis' | 'red_bis' | 'danger' | 'east':
                        marker_tmp1 = BuildPath.tower(shape_height/3, width/2, width/4,0)
                        marker_tmp2 = BuildPath.tower(shape_height/3, width/6, width/8, 2*shape_height/3)
                        shape_marker2 = Path.make_compound_path( marker_tmp1, marker_tmp2)
                    case 'south':
                        shape_marker2 = BuildPath.tower(shape_height/3, width/2, width/4,0)
                    case 'north':
                        shape_marker2 = BuildPath.tower(2*shape_height/3, width/4, width/8, shape_height/3)
                    case 'west':
                        shape_marker2 = BuildPath.tower(shape_height/3, width/4, width/6, shape_height/3)
                    case 'safe_water':
                        shape_marker2 = BuildPath.rectangle(shape_height, width/8, 0)
                    case 'emergency':
                        shape_marker2 = BuildPath.rectangle(shape_height, width/8, 0)
                    case _:
                        shape_marker2 = shape_marker
            case 'tower':
                shape_marker = BuildPath.tower(shape_height, width/2, 3*width/8, 0)
                match top_mark_type:
                    case 'green_bis' | 'red_bis' | 'danger' | 'east':
                        marker_tmp1 = BuildPath.tower(shape_height/3, width/2, 11*width/24, 0)
                        marker_tmp2 = BuildPath.tower(shape_height/3, 10*width/24, 3*width/8, 2*shape_height/3)
                        shape_marker2 = Path.make_compound_path( marker_tmp1, marker_tmp2)
                    case 'north':
                        shape_marker2 = BuildPath.tower(shape_height/2, 11*width/24, 3*width/8, shape_height/2)
                    case 'south':
                        shape_marker2 = BuildPath.tower(shape_height/2, width/2, 11*width/24, 0)
                    case 'west':
                        shape_marker2 = BuildPath.tower(shape_height/3, 11*width/24, 10*width/24, shape_height/3)
                    case 'safe_water':
                        shape_marker2 = BuildPath.rectangle(shape_height, width/3, 0)
                    case 'emergency':
                        shape_marker2 = BuildPath.rectangle(shape_height, width/3, 0)
                    case _:
                        shape_marker2 = shape_marker
            case _:
                print('not defined shape')
        return shape_marker, shape_marker2

    def select_color(self) -> tuple[str, str]:
        """ select color """
        match self.top_mark_type.lower():
            case 'green':
                color = 'green'
                color2 = 'green'
            case 'green_bis':
                color = 'red'
                color2 = 'green'
            case 'red' :
                color = 'red'
                color2 = 'red'
            case 'red_bis':
                color = 'green'
                color2 = 'red'
            case 'special':
                color ='yellow'
                color2 ='yellow'
            case 'safe_water':
                color ='white'
                color2 ='red'
            case 'danger':
                color ='red'
                color2 = 'black'
            case 'emergency':
                color = 'blue'
                color2 = 'yellow'
            case _:
                color = 'yellow'
                color2 = 'black'
        return color, color2

    def select_topmark_marker(self, size, shift_up: float):
        """ select topmark marker """
        match self.top_mark_type:
            case 'green':
                topmark_marker = BuildPath.green_topmark(size, shift_up)
            case 'green_bis':
                topmark_marker = BuildPath.green_topmark(size, shift_up)
            case 'red':
                topmark_marker = BuildPath.red_topmark(height=size*2, width=size*2, shift_up=shift_up)
            case 'red_bis':
                topmark_marker = BuildPath.red_topmark(height=size*2, width=size*2, shift_up=shift_up)
            case 'south':
                topmark_marker = BuildPath.south_topmark(size, shift_up)
            case 'north':
                topmark_marker = BuildPath.north_topmark(size, shift_up)
            case 'east':
                topmark_marker = BuildPath.east_topmark(size, shift_up)
            case 'west':
                topmark_marker = BuildPath.west_topmark(size, shift_up)
            case 'danger':
                topmark_marker = BuildPath.danger_topmark(size, shift_up)
            case 'special':
                topmark_marker = BuildPath.diagonal_cross(shift_up + size, size)
            case 'safe_water':
                topmark_marker = BuildPath.circle(size, shift_up + size)
            case 'emergency':
                topmark_marker = BuildPath.cross(shift_up + size, size)
            case _:
                print(' Not a valid topmark')
        line_path = Path([(0,shift_up-size/2), (0,shift_up)], [1,2])
        topmark_marker = Path.make_compound_path(topmark_marker, line_path)
        return topmark_marker

class BuildPath:
    """ Build path"""
    @staticmethod
    def triangle(width : float, height : float, shift_up : float) -> Path:
        """ Build a triangle path """
        vertices = [(-width/2, shift_up), (0, shift_up + height), (width/2, shift_up), (-width/2, shift_up)]
        codes = [1, 2, 2, 79]
        triangle = Path(vertices,codes)
        return triangle
    
    @staticmethod
    def triangle_down(size : float, shift_up : float) -> Path:
        """ Build a triangle path """
        vertices = [(0, shift_up), (-size, shift_up + 2*size), (size, shift_up + 2*size), (0, shift_up)]
        codes = [1, 2, 2, 79]
        triangle_path = Path(vertices,codes)
        return triangle_path
    
    @staticmethod
    def rectangle(height : float, width : float, shift_up: float) -> Path:
        """ Build a rectangle path """
        vertices = [(-width/2, shift_up), (-width/2, height + shift_up),
                    (width/2, height + shift_up), (width/2, shift_up), (-width/2, shift_up)]
        codes = [1, 2, 2, 2, 79]
        rectangle_path = Path(vertices,codes)
        return rectangle_path

    @staticmethod
    def conical(height : float, width : float) -> Path:
        """ Buils conocal curved path"""
        vertices =[(-width/2,0), (-width/2, height/3), (0,height), (width/2, height/3), (width/2,0),(-width/2,0)]
        codes = [1,3,2,3,2,79]
        conical_path = Path(vertices,codes)
        return conical_path
    
    @staticmethod
    def pillar(height, width) -> Path:
        """ Buils pillar path"""
        vertices =[(-width/2,0), (-width/4, height/3), (-width/8,height),(width/8,height), (width/4, height/3), (width/2,0),(-width/2,0)]
        codes = [1,2,2,2,2,2,79]
        pillar_path = Path(vertices,codes)
        return pillar_path

    @staticmethod
    def diagonal_cross(height, width) -> Path:
        """ Build diagonal cross path """
        vertices = [(width/3*0, width/3*1 + height), (width/3*2, width/3*3 + height), (width/3*3, width/3*2 + height),
            (width/3*1, width/3*0 + height), (width/3*3, width/3*-2 + height), (width/3*2, width/3*-3 + height),
            (width/3*0, width/3*-1 + height), (width/3*-2, width/3*-3 + height), (width/3*-3, width/3*-2 + height),
            (width/3*-1, width/3*0 + height), (width/3*-3, width/3*2 + height), (width/3*-2, width/3*3 + height), (width/3*0, width/3*1 + height)]
        codes = [1,2,2,2,2,2,2,2,2,2,2,2,79]
        cross_path = Path(vertices, codes)
        return cross_path

    @staticmethod
    def cross(height, width) -> Path:
        """ Build horizontal cross path """
        vertices = [(width/4, width/4 + height), (width, width/4 + height), (width, -width/4 + height), (width/4, -width/4 + height),
            (width/4, -width + height), (-width/4, -width + height), (-width/4, -width/4 + height),
            (-width, -width/4 + height), (-width, width/4 + height), (-width/4, width/4 + height),
            (-width/4, width/4 + height), (-width/4, width + height), (width/4, width + height), (width/4, width/4 + height)]
        codes = [1,2,2,2,2,2,2,2,2,2,2,2,2,79]
        cross_path = Path(vertices, codes)
        return cross_path

    @staticmethod
    def tower(height, width_botton, width_top, shift_up) -> Path:
        """ build tower path """
        vertices = [(-width_botton, shift_up), (-width_top, height + shift_up), (width_top, height + shift_up), (width_botton,shift_up), (-width_botton,shift_up)]
        codes = [1, 2, 2, 2, 79]
        tower_path = Path(vertices, codes)
        return tower_path

    @staticmethod
    def church() -> Path:
        """ Build church path """
        vertices = [(0,0), (0,2), (-1,3), (1,3), (0,2), (0,0), (2,0), (3,1), (3,-1), (2,0),
            (0,0), (0,-2), (1,-3), (-1,-3), (0,-2), (0,0), (-2,0), (-3,-1), (-3,1), (-2,0), (0,0)]
        codes=[1,3,2,2,3, 2,3,2,2,3, 2,3,2,2,3, 2,3,2,2,3, 79]
        church_path = Path(vertices, codes)
        return church_path
    
    @staticmethod
    def land_tower(height, width) -> Path:
        """ build tower path """
        botton_tower_path = BuildPath.tower(height*3/4, width, width/2, 0)
        top_tower_path = BuildPath.rectangle(height/4,width,height*3/4)
        land_tower_path = Path.make_compound_path(botton_tower_path, top_tower_path)
        return land_tower_path
    
    @staticmethod
    def water_tower(height, width) -> Path:
        """ build tower path """
        botton_tower_path = BuildPath.tower(height*3/4, width, width/2, 0)
        top_tower_path = BuildPath.rectangle(height/4, 2*width, height*3/4)
        land_tower_path = Path.make_compound_path(botton_tower_path, top_tower_path)
        return land_tower_path
    
    @staticmethod
    def wreck() -> Path:
        """ build wreck path"""
        vertices =[(-2,0), (-3,2), (3,0), (-2,0)]
        codes = [1,2,2,79]
        boat_path = Path(vertices, codes)
        mast_path = Path([(0,0), (1,3)], [1,2])
        ref_line_path = Path([(-3,0), (3.5,0) ],[1,2])
        wreck_path = Path.make_compound_path(boat_path, mast_path, ref_line_path)
        return wreck_path
    
    @staticmethod
    def wreck_depth() -> Path:
        """ build wreck path"""
        vertices =[(-2,0), (2,0), (0,1), (0,-1), (-1,0.5), (-1,-0.5), (1,0.5), (1,-0.5)]
        codes = [1,2,1,2,1,2,1,2]
        wreck_depth_path = Path(vertices, codes)
        return wreck_depth_path

    @staticmethod
    def light(angle) -> Path:
        """ build light path """
        vertices = [(1,0), (6,1), (6.5, 0.9), (6.8,0.7), (7,0), (6.8,-0.7 ), (6.5, -0.9), (6,-1),(6,0)]
        codes = [1,2,3,3,2,3,3,2,79]
        light_path = Path(vertices,codes)
        light_path = light_path.transformed(transforms.Affine2D().rotate(angle))
        return light_path

    @staticmethod
    def spherical(width : float, angle_start: float, angle_stop: float, shift_up: float) -> Path:
        """ Build spherical path"""
        tmp = Path.arc(angle_start,angle_stop)
        vertices = tmp.vertices*width
        for vertice in vertices:
            vertice[1]=vertice[1] + shift_up
        codes = tmp.codes
        spherical_path = Path(vertices, codes)
        return spherical_path

    @staticmethod
    def circle(size: float, shift_up: float) -> Path:
        """ Build circle path """
        circle = Path.circle([0.0, shift_up], size)
        return circle
    
    @staticmethod
    def green_topmark(size: float, shift_up: float) -> Path:
        """ plot green beacon """
        triangle_marker = BuildPath.triangle(2*size, 2*size, shift_up)
        return triangle_marker
    
    @staticmethod
    def red_topmark(height: float, width: float, shift_up: float) -> Path:
        """ Plot red beacon """
        red_marker = BuildPath.rectangle(height, width, shift_up)
        return red_marker
    @staticmethod
    
    def north_topmark(size: float, shift_up: float) -> Path:
        """ Plot north beacon """
        triangle_marker1 = BuildPath.triangle(2*size, 2*size, shift_up)
        triangle_marker2 = BuildPath.triangle(2*size, 2*size, shift_up + 2*size + size/2)
        north_marker = Path.make_compound_path(triangle_marker1, triangle_marker2)
        return north_marker
    
    @staticmethod
    def south_topmark(size: float, shift_up: float) -> Path:
        """ Plot north beacon """
        triangle_marker1 = BuildPath.triangle_down(size, shift_up)
        triangle_marker2 = BuildPath.triangle_down(size, shift_up + 2*size + size/2)
        south_marker = Path.make_compound_path(triangle_marker1, triangle_marker2)
        return south_marker
    
    @staticmethod
    def east_topmark(size: float, shift_up: float) -> Path:
        """ Plot east beacon """
        triangle_marker1 = BuildPath.triangle_down(size, shift_up)
        triangle_marker2 = BuildPath.triangle(2*size, 2*size, shift_up + 2*size + size/2)
        east_marker = Path.make_compound_path(triangle_marker1, triangle_marker2)
        return east_marker
        
    @staticmethod
    def west_topmark(size: float, shift_up: float) -> Path:
        """ Plot west beacon """
        triangle_marker1 = BuildPath.triangle(2*size, 2*size, shift_up)
        triangle_marker2 = BuildPath.triangle_down(size, shift_up + 2*size + size/2)
        west_marker = Path.make_compound_path(triangle_marker1, triangle_marker2)
        return west_marker
    
    @staticmethod
    def danger_topmark(size: float, shift_up: float) -> Path:
        """ Plot danger beacon """
        circle_marker1 = BuildPath.circle(size, shift_up + size)
        circle_marker2 = BuildPath.circle(size, shift_up + 3*size)
        return Path.make_compound_path(circle_marker1, circle_marker2)

    @staticmethod
    def marina() -> Path:
        """ Build marina mark"""
        tmp0 = Path.arc(-20,200)
        tmp1 = Path.arc(210,-30)
        mast = Path([(0,-0.5),(0,1)] , [1, 2])
        tmp2 = Path([(-0.866,-0.5),(0.866,-0.5)] , [1, 2])
        sail1 = Path([(0, -0.5), (0.9, -0.3), (0.4, 0.4), (0.4, 0.9), (0, 0.7), (0, -0.5)], [1,2,3,2,2,79])
        sail2 = Path([(-0.866, -0.5), (-0.5, 0.5), (0, 0.9), (-0.2,0.2), (0, -0.4), (-0.5,-0.3), (-0.866, -0.5)], [1,3,2,3,2,3,2])
        marina_marker = Path.make_compound_path(tmp1, tmp2, mast, tmp0, sail1, sail2)
        return marina_marker

    @staticmethod
    def anchorage() -> Path:
        """ Build anchorage mark """
        tmp1 = Path.arc(210,-30)
        tmp2 = Path([(0, -1),(0, 0.8)], [1, 2])
        tmp3 = Path([(-0.4, 0.6), (0.4, 0.6)] , [1, 2])
        tmp4 = BuildPath.circle(0.2, 1)
        tmp5 = Path([(-0.86, -0.86), (-0.86, -0.5), (-0.5, -0.5)], [1, 2, 2])
        tmp6 = Path([(0.86, -0.86), (0.86, -0.5), (0.5, -0.5)], [1, 2, 2])
        marker = Path.make_compound_path(tmp1, tmp2, tmp3, tmp4, tmp5, tmp6 )
        return marker
    
    @staticmethod
    def no_anchorage() -> Path:
        """ Build anchorage mark """
        tmp1 = BuildPath.anchorage()
        tmp2 = Path([(-1, -1),(1, 1)], [1, 2])
        tmp3 = Path([(-1, 1),(1, -1)], [1, 2])
        return Path.make_compound_path(tmp1, tmp2, tmp3)
    
    @staticmethod
    def fish() -> Path:
        """ Build anchorage mark """
        tmp1 = Path([(-1, -0.5), (0.5, 1), (1, 0), (0.5, -1), (-1, 0.5)], [1, 3, 3, 3, 2])
        tmp2 = Path([(0.5, 0.42), (0.5,-0.42)], [1,2])
        tmp3 = Path.circle([0.7, 0.15], 0.02)
        return Path.make_compound_path(tmp1, tmp2, tmp3)
    
    @staticmethod
    def no_fish():
        """ Build anchorage mark """
        tmp1 = BuildPath.fish()
        tmp2 = Path([(-1, -1),(1, 1)], [1, 2])
        tmp3 = Path([(-1, 1),(1, -1)], [1, 2])
        fish_marker = Path.make_compound_path(tmp1, tmp2, tmp3)
        return fish_marker

    @staticmethod
    def slipway():
        return Path([(-2,1), (-2, 0), (2,0), (-2,1)] ,[1, 2, 2, 79])

    @staticmethod
    def steps():
        return Path([(-3, 2), (-1, 2), (-1, 1), (0, 1), (0, 0), (1, 0), (1, -1), 
                     (2, -1), (2, -2), (4, -2), (4, -3), (1, -3), (-3, 1), (-3, 2)], 
                    [1,2,2,2,2,2,2,2,2,2,2,2,2,79])

def main():

    PlotMark.markersize = 100

    plt.figure(1,figsize=(10,5) )
    for j, shape in enumerate(SEAMARK_SET):
        plt.text(1,j*2,shape.capitalize(), horizontalalignment='center')

    for i, topmark in enumerate(TopMark):
        plt.text(i+2,len(SEAMARK_SET)*2, topmark.name.capitalize(),
                 horizontalalignment='left', rotation = 30)
        for j, shape in enumerate(SEAMARK_SET):
            PlotMark(i+2, j*2, shape, topmark.name, floating=False)
    plt.title('Sea marks as a function of shape and topmark')
    
    
    plt.plot(1,13,'*')
    plt.axis('off')
    #plt.show(block="True")
    plt.draw()

    plt.figure(2)
    

    plt.text(1,15,'Land marks')
    for i, mark in enumerate(LANDMARKS_SET):
        plt.text(i*2 + 4,16,mark.capitalize(), horizontalalignment='left', rotation = 30)
        land_mark = PlotMark(i*2+4, 15, mark)
    
    plt.text(1, 19,'Danger marks')
    for i, mark in enumerate(DANGERS_SET):
        plt.text(i*2 + 4,20,mark.capitalize(), horizontalalignment='left', rotation = 30)
        danger_mark = PlotMark(i*2+4,19,mark)
    
    #plt.text(1, 23, 'Light')
        
    PlotMark(3, 23,'Spar','East',light_color='yellow', floating=True)
        
    plt.plot(1, 25, '*')
    
    PlotMark(5, 23, 'marina')
    PlotMark(7, 23, 'anchorage')
    PlotMark(9, 23, 'fish')
    PlotMark(9, 23, 'no_fish')
    PlotMark(11, 23, 'slipway')
    PlotMark(13, 23, 'steps')
    plt.axis('off')
    plt.title('Nautical symbols')
    plt.show()
    

if __name__ == "__main__":
    
    main()
