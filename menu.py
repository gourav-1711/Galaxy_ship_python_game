from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock


class MenuUi(RelativeLayout):
    
    gradient_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._create_gradient_texture()
        self._bg_rect = None
        self._bg_color = None
        # Schedule initial draw after kv rules have been applied
        Clock.schedule_once(self._draw_gradient, 0)
        self.bind(size=self._update_bg_rect, pos=self._update_bg_rect)

    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super(RelativeLayout , self).on_touch_down(touch)

    def _create_gradient_texture(self):
        """Create a vertical gradient texture from dark purple (bottom) to dark blue (top)."""
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
        """Draw gradient background once."""
        with self.canvas.before:
            self._bg_color = Color(1, 1, 1, 0.8)
            self._bg_rect = Rectangle(
                texture=self.gradient_texture, pos=self.pos, size=self.size
            )

    def _update_bg_rect(self, *args):
        """Update gradient rect position/size on resize."""
        if self._bg_rect:
            self._bg_rect.pos = self.pos
            self._bg_rect.size = self.size

    def on_settings_press(self):
        """Handle settings icon press — placeholder."""
        print("Settings pressed")
