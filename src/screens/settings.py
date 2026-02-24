from kivy.storage.jsonstore import JsonStore
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock


# 6 color presets: White, Cyan, Magenta, Lime, Gold, Coral
COLOR_PRESETS = [
    (1, 1, 1, 1),  # White
    (0, 0.9, 1, 1),  # Cyan
    (1, 0.2, 0.6, 1),  # Magenta / Hot Pink
    (0.3, 1, 0.3, 1),  # Lime Green
    (1, 0.85, 0.2, 1),  # Gold
    (1, 0.45, 0.3, 1),  # Coral / Orange
]


class SettingsScreen(RelativeLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._create_gradient_texture()
        self._bg_rect = None
        self._bg_color = None
        Clock.schedule_once(self._draw_gradient, 0)
        self.bind(size=self._update_bg_rect, pos=self._update_bg_rect)

    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super(RelativeLayout, self).on_touch_down(touch)

    def _create_gradient_texture(self):
        """Dark gradient overlay similar to other screens."""
        width = 1
        height = 256
        texture = Texture.create(size=(width, height), colorfmt="rgba")

        buf = []
        for y in range(height):
            t = y / (height - 1)
            r = int(15 + (10 - 15) * t)
            g = int(5 + (10 - 5) * t)
            b = int(35 + (50 - 35) * t)
            a = 255
            buf.extend([r, g, b, a])

        buf = bytes(buf)
        texture.blit_buffer(buf, colorfmt="rgba", bufferfmt="ubyte")
        self.gradient_texture = texture

    def _draw_gradient(self, dt):
        with self.canvas.before:
            self._bg_color = Color(1, 1, 1, 0.92)
            self._bg_rect = Rectangle(
                texture=self.gradient_texture, pos=self.pos, size=self.size
            )

    def _update_bg_rect(self, *args):
        if self._bg_rect:
            self._bg_rect.pos = self.pos
            self._bg_rect.size = self.size

    def set_lines_color(self, index):
        self.parent.lines_color = list(COLOR_PRESETS[index])
        self.save_colors()

    def set_tiles_color(self, index):
        self.parent.tiles_color = list(COLOR_PRESETS[index])
        self.save_colors()

    def set_ship_color(self, index):
        self.parent.ship_color = list(COLOR_PRESETS[index])
        self.save_colors()

    def go_back(self):
        self.parent.click_sound.play()
        self.opacity = 0
        self.parent.menu.opacity = 1

    def save_colors(self):
        self.parent.color_store.put(
            "tiles_color", tiles_color=list(self.parent.tiles_color)
        )
        self.parent.color_store.put(
            "ship_color", ship_color=list(self.parent.ship_color)
        )
        self.parent.color_store.put(
            "lines_color", lines_color=list(self.parent.lines_color)
        )
