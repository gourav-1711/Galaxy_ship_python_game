from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Line ,Color
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
    v_l_number = 10

    horizontal_lines = []
    h_l_spacing = 0.2
    h_l_number = 15

    offset_y = 0
    SPEED = 4

    speed_x = 10
    current_speed_x = 0
    offset_x = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("MainUi initialized")
        # print(f"width: {self.width}, height: {self.height}")
        self.init_vertical_lines()
        self.init_horizontal_lines()

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        
        Clock.schedule_interval(self.update, 1.0/60.0)

    
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

    def get_line_x_from_index(self, index):
        center_x = self.perspective_point_x
        spacing = self.v_l_spacing * self.width
        offset = index - 0.5
        line_x = center_x + offset * spacing + self.offset_x
        return line_x

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1,1,1)
            for i in range(self.h_l_number):
                self.horizontal_lines.append(Line())
            # self.Line = Line(points=[0, 0, 0, 0])
    
    def update_horizontal_lines(self):
        center_x = self.width/2 
        spacing = self.v_l_spacing * self.width
        offset = -int(self.v_l_number / 2)+0.5

        x_min = center_x - offset * spacing + self.offset_x
        x_max = center_x + offset * spacing + self.offset_x
        spacing_y = self.h_l_spacing * self.height
        
        for i in range(self.h_l_number):
            line_y = i * spacing_y - self.offset_y 
            x1 , y1 = self.transform(x_min, line_y)
            x2 , y2 = self.transform(x_max, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]
            

    def on_size(self , *args):
        # print(f"width: {self.width}, height: {self.height}")
        pass
        

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
        self.offset_y += self.SPEED * time_factor


        spacing_y = self.h_l_spacing * self.height
        if self.offset_y >= spacing_y:
            self.offset_y = 0

        # spacing_x = self.v_l_spacing * self.width
        self.offset_x += self.current_speed_x * time_factor
        # if self.offset_x >= spacing_x:
        #     self.offset_x = 0

class Galaxy(App):
    pass

Galaxy().run()