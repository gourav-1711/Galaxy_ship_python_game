from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')
import random
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Line ,Color, Quad , Triangle
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.core.window import Window


class MainUi(Widget):
    from transform import transform , transform_2D , transform_perspective
    from controls import is_desktop , keyboard_closed , on_keyboard_down , on_keyboard_up , on_touch_down , on_touch_up
    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    vertical_lines = []
    v_l_spacing = 0.25
    v_l_number = 8

    horizontal_lines = []
    h_l_spacing = 0.2
    h_l_number = 15

    current_y_loop = 0

    offset_y = 0
    SPEED = 1.0

    speed_x = 3.0
    current_speed_x = 0
    offset_x = 0

    nb_tiles = 10
    tiles = []
    tiles_coordinates = []

    ship = None
    ship_base_y = 0.04
    ship_height = 0.04
    ship_width = 0.1
    ship_coordinates = [(0,0), (0,0), (0,0)]
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("MainUi initialized")
        # print(f"width: {self.width}, height: {self.height}")
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.genrate_tiles_coordinates()
        self.init_ship()

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        
        Clock.schedule_interval(self.update, 1.0/60.0)

    def check_ship_collision(self):
        for i in range(0 , len(self.tiles_coordinates)):
            ti_x , ti_y = self.tiles_coordinates[i]
            if ti_y > self.current_y_loop+1:
                return False
            if self.check_ship_collision_with_tile(ti_x , ti_y):
                return True
        return False

    def game_over(self):
        print("Game Over")
        self.SPEED = 0
        self.speed_x = 0

    def check_ship_collision_with_tile(self , ti_x , ti_y):
        xmin , ymin = self.get_tile_coordinates(ti_x , ti_y)
        xmax , ymax = self.get_tile_coordinates(ti_x+1 , ti_y+1)

        for i in range(3):
            ship_x , ship_y = self.ship_coordinates[i]
            if ship_x >= xmin and ship_x <= xmax and ship_y >= ymin and ship_y <= ymax:
                return True
        return False

    def init_ship(self):
        with self.canvas:
            Color(1,0,0)
            self.ship = Triangle()

    def update_ship(self):
        center_x = self.width/2
        base_y = self.ship_base_y * self.height
        width_half = self.ship_width * self.width / 2 
        height = self.ship_height * self.height
        
        self.ship_coordinates[0] = (center_x-width_half, base_y)
        self.ship_coordinates[1] = (center_x, base_y+height)
        self.ship_coordinates[2] = (center_x+width_half, base_y)
        x1 , y1 = self.transform(*self.ship_coordinates[0])
        x2 , y2 = self.transform(*self.ship_coordinates[1])
        x3 , y3 = self.transform(*self.ship_coordinates[2])
        self.ship.points = [x1 , y1 , x2 , y2 , x3 , y3]

    def init_vertical_lines(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(self.v_l_number):
                self.vertical_lines.append(Line())
            # self.Line = Line(points=[0, 0, 0, 0])
    
    def update_vetical_lines(self):
        start_index = -int(self.v_l_number/2)+1
        for i in range(start_index , start_index + self.v_l_number):
            line_x = self.get_line_x_from_index(i)
            x1 , y1 = self.transform(line_x, 0)
            x2 , y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(self.h_l_number):
                self.horizontal_lines.append(Line())
            # self.Line = Line(points=[0, 0, 0, 0])
    
    def update_horizontal_lines(self):
        start_index = -int(self.v_l_number/2)+1
        end_index = start_index + self.v_l_number - 1

        x_min = self.get_line_x_from_index(start_index)
        x_max = self.get_line_x_from_index(end_index)
        
        for i in range(self.h_l_number):
            line_y = self.get_line_y_from_index(i)
            x1 , y1 = self.transform(x_min, line_y)
            x2 , y2 = self.transform(x_max, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def get_line_x_from_index(self, index):
        center_x = self.perspective_point_x
        spacing = self.v_l_spacing * self.width
        offset = index - 0.5
        line_x = center_x + offset * spacing + self.offset_x
        return line_x

    def get_line_y_from_index(self, index):
        spacing_y = self.h_l_spacing * self.height
        line_y = index * spacing_y - self.offset_y
        return line_y

    def get_tile_coordinates(self , ti_x , ti_y):
        ti_y = ti_y - self.current_y_loop
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x , y

    def on_size(self , *args):
        # print(f"width: {self.width}, height: {self.height}")
        pass
        
    def init_tiles(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(0 , self.nb_tiles):
                self.tiles.append(Quad())

    def genrate_tiles_coordinates(self):
        last_y = 0
        last_x = 0
        start_index = -int(self.v_l_number/2)+1
        end_index = start_index + self.v_l_number - 1
        for i in range(len(self.tiles_coordinates)-1 , -1 , -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]

        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_y = last_coordinates[1]+1
            last_x = last_coordinates[0]

        for i in range(len(self.tiles_coordinates) , self.nb_tiles):
            random_x = random.randint(0 , 2)
            # 0 = center
            # 1 = right
            # 2 = left
            start_index = -int(self.v_l_number/2)+1
            end_index = start_index + self.v_l_number - 1
            # TILES LIMIT FROM GOING LEFT AND RIGHT
            if last_x <= start_index:
                random_x = 1
            if last_x >= end_index-1:
                random_x = 2

            # Straight Line Start
            if last_y < 7:
                random_x = 0

            self.tiles_coordinates.append((last_x , last_y))
            if random_x == 1:
                last_x += 1
                self.tiles_coordinates.append((last_x , last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x , last_y))
            if random_x == 2:
                last_x -= 1
                self.tiles_coordinates.append((last_x , last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x , last_y))
            last_y += 1


    def update_tiles(self):
        for i in range(0 , self.nb_tiles):
            tile = self.tiles[i]
            tile_coordinates = self.tiles_coordinates[i]
            xmin , ymin = self.get_tile_coordinates(tile_coordinates[0] , tile_coordinates[1])
            xmax , ymax = self.get_tile_coordinates(tile_coordinates[0]+1 , tile_coordinates[1]+1)

            x1 , y1 = self.transform(xmin , ymin)
            x2 , y2 = self.transform(xmin , ymax)
            x3 , y3 = self.transform(xmax , ymax)
            x4 , y4 = self.transform(xmax , ymin)

            tile.points = [x1 , y1 , x2 , y2 , x3, y3 ,x4, y4]

        
    def on_perspective_point_x(self , widget , value):
        # print(f"X: {value}")
        pass

    def on_perspective_point_y(self , widget , value):
        # print(f"Y: {value}")
        pass

    def update(self , dt):
        # print(dt)
        time_factor = dt * 60
        self.update_vetical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_ship()
        # HORIZONTAL SPEED 
        speed_y = self.SPEED * self.height / 100
        self.offset_y += speed_y * time_factor


        spacing_y = self.h_l_spacing * self.height
        if self.offset_y >= spacing_y:
            self.offset_y = 0
            self.current_y_loop += 1
            self.genrate_tiles_coordinates()

        # VERTICAL SPEED
        speed_x = self.current_speed_x * self.width /100
        self.offset_x += speed_x * time_factor
        
        if not self.check_ship_collision():
            self.game_over()

class Galaxy(App):
    pass

Galaxy().run()