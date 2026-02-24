from kivy.core.audio import SoundLoader

def init_audio(self):
    self.menu_sound = SoundLoader.load("assets/audio/menu.mp3")
    self.begin_sound = SoundLoader.load("assets/audio/begin.wav")
    self.galaxy_sound = SoundLoader.load("assets/audio/galaxy.wav")
    self.game_over_impact_sound = SoundLoader.load(
        "assets/audio/gameover_impact.wav"
    )
    self.game_over_impact_sound.volume = 0.35
    self.game_over_sound = SoundLoader.load("assets/audio/gameover_voice.wav")
    self.game_music_sound = SoundLoader.load("assets/audio/music1.wav")
    self.restart_sound = SoundLoader.load("assets/audio/restart.wav")
    self.click_sound = SoundLoader.load("assets/audio/click.wav")

    self.menu_sound.volume = 1
    self.game_music_sound.volume = 1
    self.begin_sound.volume = 0.15
    self.game_over_sound.volume = 0.35
    self.galaxy_sound.volume = 0.15
    self.game_over_impact_sound.volume = 0.35
    self.restart_sound.volume = 0.5
    self.click_sound.volume = 0.8