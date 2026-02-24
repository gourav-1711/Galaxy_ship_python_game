from kivy.graphics import Color, Quad
import random


def init_tiles(self):
    with self.canvas:
        self.tiles_color_instruction = Color(*self.tiles_color[:3])
        for i in range(0, self.nb_tiles):
            self.tiles.append(Quad())


def genrate_tiles_coordinates(self):
    last_y = 0
    last_x = 0
    start_index = -int(self.v_l_number / 2) + 1
    end_index = start_index + self.v_l_number - 1
    for i in range(len(self.tiles_coordinates) - 1, -1, -1):
        if self.tiles_coordinates[i][1] < self.current_y_loop:
            del self.tiles_coordinates[i]

    if len(self.tiles_coordinates) > 0:
        last_coordinates = self.tiles_coordinates[-1]
        last_y = last_coordinates[1] + 1
        last_x = last_coordinates[0]

    for i in range(len(self.tiles_coordinates), self.nb_tiles):
        random_x = random.randint(0, 2)
        # 0 = center
        # 1 = right
        # 2 = left
        start_index = -int(self.v_l_number / 2) + 1
        end_index = start_index + self.v_l_number - 1
        # TILES LIMIT FROM GOING LEFT AND RIGHT
        if last_x <= start_index:
            random_x = 1
        if last_x >= end_index - 1:
            random_x = 2

        # Straight Line Start
        if last_y < 7:
            random_x = 0

        self.tiles_coordinates.append((last_x, last_y))
        if random_x == 1:
            last_x += 1
            self.tiles_coordinates.append((last_x, last_y))
            last_y += 1
            self.tiles_coordinates.append((last_x, last_y))
        if random_x == 2:
            last_x -= 1
            self.tiles_coordinates.append((last_x, last_y))
            last_y += 1
            self.tiles_coordinates.append((last_x, last_y))
        last_y += 1


def update_tiles(self):
    self.tiles_color_instruction.rgb = self.tiles_color[:3]
    for i in range(0, self.nb_tiles):
        tile = self.tiles[i]
        tile_coordinates = self.tiles_coordinates[i]
        xmin, ymin = self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])
        xmax, ymax = self.get_tile_coordinates(
            tile_coordinates[0] + 1, tile_coordinates[1] + 1
        )

        x1, y1 = self.transform(xmin, ymin)
        x2, y2 = self.transform(xmin, ymax)
        x3, y3 = self.transform(xmax, ymax)
        x4, y4 = self.transform(xmax, ymin)

        tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]


def get_tile_coordinates(self, ti_x, ti_y):
    ti_y = ti_y - self.current_y_loop
    x = self.get_line_x_from_index(ti_x)
    y = self.get_line_y_from_index(ti_y)
    return x, y
