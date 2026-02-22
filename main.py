from kivy.config import Config

Config.set("graphics", "width", "900")
Config.set("graphics", "height", "400")
from kivy.app import App, Builder
from kivy.clock import Clock
from kivy.graphics import Color, Triangle
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty, BooleanProperty
from kivy.core.window import Window
from menu import MenuUi
from kivy.properties import ObjectProperty
from kivy.core.audio import SoundLoader

Builder.load_file("menu.kv")
Builder.load_file("restart.kv")
from kivy.core.text import LabelBase, DEFAULT_FONT

LabelBase.register(DEFAULT_FONT, fn_regular="assets/fonts/Eurostile.ttf")


class MainUi(RelativeLayout):
    from transform import transform, transform_2D, transform_perspective
    from controls import (
        is_desktop,
        keyboard_closed,
        on_keyboard_down,
        on_keyboard_up,
        on_touch_down,
        on_touch_up,
    )
    from land_tiles import (
        init_tiles,
        update_tiles,
        genrate_tiles_coordinates,
        get_tile_coordinates,
    )
    from lines_gen import (
        init_vertical_lines,
        update_vetical_lines,
        init_horizontal_lines,
        update_horizontal_lines,
        get_line_x_from_index,
        get_line_y_from_index,
    )

    menu = ObjectProperty()
    restart = ObjectProperty()

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
    SPEED = 0.8

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
    ship_coordinates = [(0, 0), (0, 0), (0, 0)]

    game_over_state = BooleanProperty(False)
    game_started = BooleanProperty(False)
    game_paused = BooleanProperty(False)

    high_score = NumericProperty(0)
    main_high_score = NumericProperty(0)

    galaxy_sound = None
    game_over_impact_sound = None
    game_over_sound = None
    begin_sound = None
    game_music_sound = None
    restart_sound = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # print("MainUi initialized")
        # print(f"width: {self.width}, height: {self.height}")
        self.init_audio()
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.genrate_tiles_coordinates()
        self.init_ship()
        self.galaxy_sound.play()

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def game_start(self):
        self.reset_game()
        self.game_started = True
        self.menu.opacity = 0
        self.begin_sound.play()
        self.game_music_sound.play()
        self.game_music_sound.loop = True
        self.game_music_sound.volume = 1
        self.restart.opacity = 0

    def game_over(self):
        # Play game over sound after 0.5 seconds
        Clock.schedule_once(self.play_game_over_sound, 0.5)
        # Reduce music volume
        self.game_music_sound.volume = 0.1
        # Update high score
        if self.high_score > self.main_high_score:
            self.main_high_score = self.high_score
        # Show restart button
        self.restart.opacity = 1

    def play_game_over_sound(self, dt):
        if self.game_over_state:
            self.game_over_sound.play()

    def toggle_pause(self):
        self.game_paused = not self.game_paused
        if self.game_paused:
            self.game_music_sound.volume = 0.2
        else:
            self.game_music_sound.volume = 1

    def show_menu(self):
        self.reset_game()
        self.menu.opacity = 1
        self.restart.opacity = 0
        Clock.schedule_once(lambda dt: self.game_music_sound.stop(), 0.1)

    def reset_game(self):
        # Reload short sounds to get fresh GStreamer pipelines.
        # GStreamer one-shot sounds can't replay reliably after stop() —
        # reloading is the cleanest fix.
        self.game_over_impact_sound = SoundLoader.load(
            "assets/audio/gameover_impact.wav"
        )
        self.game_over_impact_sound.volume = 0.35
        self.game_over_sound = SoundLoader.load("assets/audio/gameover_voice.wav")
        self.game_over_sound.volume = 0.35

        # Stop music so a future menu sound can be played from show_menu()
        # self.game_music_sound.stop()

        self.tiles_coordinates = []
        self.current_y_loop = 0
        self.offset_y = 0
        self.SPEED = 0.8
        self.speed_x = 3.0
        self.current_speed_x = 0
        self.offset_x = 0
        self.high_score = 0
        self.game_started = False
        self.genrate_tiles_coordinates()

        self.game_over_state = False

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

        # ship_center_x , ship_center_y = self.ship_coordinates[1][0] , self.ship_coordinates[0][1]
        # if ship_center_x >= xmin and ship_center_x <= xmax and ship_center_y >= ymin and ship_center_y <= ymax:
        #     return True

        for i in range(3):
            ship_x, ship_y = self.ship_coordinates[i]
            if ship_x >= xmin and ship_x <= xmax and ship_y >= ymin and ship_y <= ymax:
                return True
        return False

    def init_ship(self):
        with self.canvas:
            Color(1, 0, 0)
            self.ship = Triangle()

    def update_ship(self):
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

    def on_size(self, *args):
        # print(f"width: {self.width}, height: {self.height}")
        pass

    def on_perspective_point_x(self, widget, value):
        # print(f"X: {value}")
        pass

    def on_perspective_point_y(self, widget, value):
        # print(f"Y: {value}")
        pass

    def init_audio(self):
        self.begin_sound = SoundLoader.load("assets/audio/begin.wav")
        self.galaxy_sound = SoundLoader.load("assets/audio/galaxy.wav")
        self.game_over_impact_sound = SoundLoader.load(
            "assets/audio/gameover_impact.wav"
        )
        self.game_over_sound = SoundLoader.load("assets/audio/gameover_voice.wav")
        self.game_music_sound = SoundLoader.load("assets/audio/music1.wav")
        self.restart_sound = SoundLoader.load("assets/audio/restart.wav")

        self.game_music_sound.volume = 1
        self.begin_sound.volume = 0.15
        self.game_over_sound.volume = 0.35
        self.galaxy_sound.volume = 0.15
        self.game_over_impact_sound.volume = 0.35
        self.restart_sound.volume = 0.5

    def update(self, dt):
        # print(dt)
        time_factor = dt * 60
        self.update_vetical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_ship()
        # HORIZONTAL SPEED
        if not self.game_over_state and self.game_started and not self.game_paused:
            speed_y = self.SPEED * self.height / 100

            self.offset_y += speed_y * time_factor

            spacing_y = self.h_l_spacing * self.height
            while self.offset_y >= spacing_y:
                self.offset_y -= spacing_y
                self.current_y_loop += 1
                self.high_score += 1
                # print(f"high score : {self.high_score}")
                self.genrate_tiles_coordinates()

            # VERTICAL SPEED
            speed_x = self.current_speed_x * self.width / 100
            self.offset_x += speed_x * time_factor

        if (
            self.game_started
            and not self.game_paused
            and not self.check_ship_collision()
            and not self.game_over_state
        ):
            # checking sound
            self.game_over_impact_sound.play()
            # self.galaxy_sound.play()
            self.game_over_state = True
            self.game_over()


class Galaxy(App):
    pass


Galaxy().run()
