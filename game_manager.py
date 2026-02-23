from kivy.clock import Clock
from kivy.core.audio import SoundLoader

def game_start(self):
    self.reset_game()
    self.game_started = True
    self.menu.opacity = 0
    self.menu_sound.stop()
    self.click_sound.play()
    self.begin_sound.play()
    self.game_music_sound.play()
    self.game_music_sound.loop = True
    self.game_music_sound.volume = 1
    self.restart.opacity = 0
    self.pause_screen.opacity = 0
    self.settings_screen.opacity = 0

def game_over(self):
    # Play game over sound after 0.5 seconds
    Clock.schedule_once(self.play_game_over_sound, 0.5)
    # Reduce music volume
    self.game_music_sound.volume = 0.1
    # Update high score
    if self.high_score > self.main_high_score:
        self.main_high_score = self.high_score
        self.high_score_store.put("high_score", high_score=self.high_score)
    # Show restart button
    self.restart.opacity = 1

def play_game_over_sound(self, dt):
    if self.game_over_state:
        self.game_over_sound.play()

def toggle_pause(self):
    self.game_paused = not self.game_paused
    if self.game_paused:
        self.game_music_sound.volume = 0.2
        self.pause_screen.opacity = 1
    else:
        self.game_music_sound.volume = 1
        self.pause_screen.opacity = 0

def show_menu(self):
    self.reset_game()
    self.menu.opacity = 1
    self.restart.opacity = 0
    self.pause_screen.opacity = 0
    self.settings_screen.opacity = 0
    self.click_sound.play()
    Clock.schedule_once(lambda dt: self.game_music_sound.stop(), 0.1)
    self.menu_sound.play()

def show_settings(self):
    self.menu.opacity = 0
    self.settings_screen.opacity = 1
    self.click_sound.play()

def reset_game(self):

    self.game_over_impact_sound = SoundLoader.load(
        "assets/audio/gameover_impact.wav"
    )
    self.game_over_impact_sound.volume = 0.35
    self.game_over_sound = SoundLoader.load("assets/audio/gameover_voice.wav")
    self.game_over_sound.volume = 0.35

    self.tiles_coordinates = []
    self.current_y_loop = 0
    self.offset_y = 0
    self.SPEED = 0.8
    self.speed_x = 3.0
    self.current_speed_x = 0
    self.offset_x = 0
    self.high_score = 0
    self.game_started = False
    self.game_paused = False
    self.genrate_tiles_coordinates()

    self.game_over_state = False
