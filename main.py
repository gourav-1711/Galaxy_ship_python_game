import sys
import os
# PyInstaller --onefile extracts to a temp dir; chdir there so all relative paths work
if getattr(sys, "frozen", False):
    # writable dir = folder the .exe lives in (for saving user data)
    EXE_DIR = os.path.dirname(sys.executable)
    os.chdir(sys._MEIPASS)
    # Force SDL2 audio — GStreamer isn't properly bundled by PyInstaller
    os.environ["KIVY_AUDIO"] = "sdl2"
else:
    EXE_DIR = os.path.dirname(os.path.abspath(__file__))

from kivy.config import Config

Config.set("graphics", "width", "900")
Config.set("graphics", "height", "400")


from kivy.app import App, Builder
from kivy.clock import Clock

# from kivy.graphics import Color, Triangle
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty, BooleanProperty, ListProperty
from kivy.core.window import Window
from src.screens.menu import MenuUi
from src.screens.pause import PauseScreen
from src.screens.settings import SettingsScreen
from kivy.properties import ObjectProperty

# from kivy.core.audio import SoundLoader

Builder.load_file("src/screens/menu.kv")
Builder.load_file("src/screens/restart.kv")
Builder.load_file("src/screens/pause.kv")
Builder.load_file("src/screens/settings.kv")
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.storage.jsonstore import JsonStore

LabelBase.register(DEFAULT_FONT, fn_regular="assets/fonts/Eurostile.ttf")


class MainUi(RelativeLayout):
    from src.game_files.transform import transform, transform_2D, transform_perspective
    from src.game_files.audio import init_audio
    from src.game_files.controls import (
        is_desktop,
        keyboard_closed,
        on_keyboard_down,
        on_keyboard_up,
        on_touch_down,
        on_touch_up,
    )
    from src.game_files.land_tiles import (
        init_tiles,
        update_tiles,
        genrate_tiles_coordinates,
        get_tile_coordinates,
    )
    from src.game_files.lines_gen import (
        init_vertical_lines,
        update_vetical_lines,
        init_horizontal_lines,
        update_horizontal_lines,
        get_line_x_from_index,
        get_line_y_from_index,
    )
    from src.game_files.game_manager import (
        game_start,
        game_over,
        play_game_over_sound,
        reset_game,
        toggle_pause,
        show_menu,
        show_settings,
    )
    from src.game_files.ship import (
        init_ship,
        update_ship,
        check_ship_collision,
        check_ship_collision_with_tile,
    )

    menu = ObjectProperty()
    restart = ObjectProperty()
    pause_screen = ObjectProperty()
    settings_screen = ObjectProperty()

    perspective_point_x = NumericProperty(0)
    perspective_point_y = NumericProperty(0)

    lines_color = ListProperty([1, 1, 1, 1])
    tiles_color = ListProperty([1, 1, 1, 1])
    ship_color = ListProperty([1, 0, 0, 1])

    vertical_lines = []
    v_l_spacing = 0.65
    v_l_number = 14

    horizontal_lines = []
    h_l_spacing = 0.35
    h_l_number = 17

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
    menu_sound = None
    click_sound = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # print("MainUi initialized")
        # print(f"width: {self.width}, height: {self.height}")
        self.high_score_store = JsonStore(os.path.join(EXE_DIR, "high_score.json"))
        self.color_store = JsonStore(os.path.join(EXE_DIR, "color.json"))

        if self.high_score_store.exists("high_score"):
            self.main_high_score = self.high_score_store.get("high_score")["high_score"]

        if self.color_store.exists("lines_color"):
            self.lines_color = self.color_store.get("lines_color")["lines_color"]
            self.tiles_color = self.color_store.get("tiles_color")["tiles_color"]
            self.ship_color = self.color_store.get("ship_color")["ship_color"]

        self.init_audio()
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.genrate_tiles_coordinates()
        self.init_ship()
        self.galaxy_sound.play()
        self.menu_sound.play()

        if self.is_desktop():
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

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
                # DECREASING TILES SPACE
                self.v_l_spacing -= 0.0002
                # INCREASING SPEED
                self.SPEED += 0.005
                self.speed_x += 0.0008

            # VERTICAL SPEED
            speed_x = self.current_speed_x * self.width / 100
            self.offset_x += speed_x * time_factor

        if (
            self.game_started
            and not self.game_paused
            and not self.check_ship_collision()
            and not self.game_over_state
        ):
            print(f"SPEED X: {self.current_speed_x} , SPEED Y: {self.SPEED}")
            # checking sound
            self.game_over_impact_sound.play()
            # self.galaxy_sound.play()
            self.game_over_state = True
            self.game_over()


class Galaxy(App):
    pass


Galaxy().run()
