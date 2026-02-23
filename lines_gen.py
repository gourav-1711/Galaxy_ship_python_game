from kivy.graphics import Color, Line


def init_vertical_lines(self):
    with self.canvas:
        self.v_lines_color_instruction = Color(*self.lines_color[:3])
        for i in range(self.v_l_number):
            self.vertical_lines.append(Line())
        # self.Line = Line(points=[0, 0, 0, 0])


def update_vetical_lines(self):
    self.v_lines_color_instruction.rgb = self.lines_color[:3]
    start_index = -int(self.v_l_number / 2) + 1
    for i in range(start_index, start_index + self.v_l_number):
        line_x = self.get_line_x_from_index(i)
        x1, y1 = self.transform(line_x, 0)
        x2, y2 = self.transform(line_x, self.height)
        self.vertical_lines[i].points = [x1, y1, x2, y2]


def init_horizontal_lines(self):
    with self.canvas:
        self.h_lines_color_instruction = Color(*self.lines_color[:3])
        for i in range(self.h_l_number):
            self.horizontal_lines.append(Line())
        # self.Line = Line(points=[0, 0, 0, 0])


def update_horizontal_lines(self):
    self.h_lines_color_instruction.rgb = self.lines_color[:3]
    start_index = -int(self.v_l_number / 2) + 1
    end_index = start_index + self.v_l_number - 1

    x_min = self.get_line_x_from_index(start_index)
    x_max = self.get_line_x_from_index(end_index)

    for i in range(self.h_l_number):
        line_y = self.get_line_y_from_index(i)
        x1, y1 = self.transform(x_min, line_y)
        x2, y2 = self.transform(x_max, line_y)
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
