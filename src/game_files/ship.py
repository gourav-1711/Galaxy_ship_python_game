from kivy.graphics import Color, Triangle

def init_ship(self):
    with self.canvas:
        self.ship_color_instruction = Color(*self.ship_color[:3])
        self.ship = Triangle()

def update_ship(self):
    self.ship_color_instruction.rgb = self.ship_color[:3]
    center_x = self.width / 2
    base_y = self.ship_base_y * self.height
    width_half = self.ship_width * self.width / 2
    height = self.ship_height * self.height

    self.ship_coordinates[0] = (center_x - width_half, base_y)
    self.ship_coordinates[1] = (center_x, base_y + height)
    self.ship_coordinates[2] = (center_x + width_half, base_y)
    x1, y1 = self.transform(*self.ship_coordinates[0])
    x2, y2 = self.transform(*self.ship_coordinates[1])
    x3, y3 = self.transform(*self.ship_coordinates[2])
    self.ship.points = [x1, y1, x2, y2, x3, y3]

    # def on_size(self, *args):
    #     # print(f"width: {self.width}, height: {self.height}")
    #     pass

    # def on_perspective_point_x(self, widget, value):
    #     # print(f"X: {value}")
    #     pass

    # def on_perspective_point_y(self, widget, value):
    # print(f"Y: {value}")
    pass


def check_ship_collision(self):
    for i in range(0, len(self.tiles_coordinates)):
        ti_x, ti_y = self.tiles_coordinates[i]
        if ti_y > self.current_y_loop + 1:
            return False
        if self.check_ship_collision_with_tile(ti_x, ti_y):
            return True
    return False

def check_ship_collision_with_tile(self, ti_x, ti_y):
    xmin, ymin = self.get_tile_coordinates(ti_x, ti_y)
    xmax, ymax = self.get_tile_coordinates(ti_x + 1, ti_y + 1)

    ship_center_x, ship_center_y = (
        self.ship_coordinates[1][0],
        self.ship_coordinates[0][1],
    )
    if (
        ship_center_x >= xmin
        and ship_center_x <= xmax
        and ship_center_y >= ymin
        and ship_center_y <= ymax
    ):
        return True

    # for i in range(3):
    #     ship_x, ship_y = self.ship_coordinates[i]
    #     if ship_x >= xmin and ship_x <= xmax and ship_y >= ymin and ship_y <= ymax:
    #         return True
    return False
