# main.py
import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window

Window.size = (600, 800)

class DogDodger(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player_size = 50
        self.player_x = Window.width // 2 - self.player_size // 2
        self.player_y = 20
        self.player_speed = 10
        self.jumping = False
        self.jump_vel = 0

        self.dogs = []
        self.score = 0

        self.score_label = Label(text="Score: 0", pos=(10, Window.height-40), size_hint=(None, None))
        self.add_widget(self.score_label)

        Clock.schedule_interval(self.update, 1/60)  # 60 FPS
        Clock.schedule_interval(self.spawn_dog, 1.5)  # spawn a dog every 1.5s

    def spawn_dog(self, dt):
        size = 30
        x = random.randint(0, int(Window.width - size))
        self.dogs.append({"x": x, "y": Window.height, "size": size})

    def on_touch_down(self, touch):
        if touch.x < Window.width / 3:  # Left side
            self.player_x -= self.player_speed
        elif touch.x > 2 * Window.width / 3:  # Right side
            self.player_x += self.player_speed
        else:  # Middle/top area = jump
            if not self.jumping:
                self.jumping = True
                self.jump_vel = 15

    def update(self, dt):
        self.canvas.clear()
        with self.canvas:
            # Draw player
            Color(0, 0, 1)
            Rectangle(pos=(self.player_x, self.player_y), size=(self.player_size, self.player_size))

            # Update dogs
            Color(0.6, 0.3, 0)  # brown
            for dog in self.dogs[:]:
                dog["y"] -= 4  # fall speed
                Rectangle(pos=(dog["x"], dog["y"]), size=(dog["size"], dog["size"]))
                if (self.player_x < dog["x"] + dog["size"] and
                    self.player_x + self.player_size > dog["x"] and
                    self.player_y < dog["y"] + dog["size"] and
                    self.player_y + self.player_size > dog["y"]):
                    self.end_game()
                if dog["y"] < 0:
                    self.dogs.remove(dog)
                    self.score += 1
                    self.score_label.text = f"Score: {self.score}"

        # Handle jump physics
        if self.jumping:
            self.player_y += self.jump_vel
            self.jump_vel -= 1
            if self.player_y <= 20:
                self.player_y = 20
                self.jumping = False

    def end_game(self):
        self.clear_widgets()
        self.add_widget(Label(text="Game Over", center=(Window.width/2, Window.height/2), font_size=40))
        Clock.unschedule(self.update)
        Clock.unschedule(self.spawn_dog)

class DogDodgerApp(App):
    def build(self):
        return DogDodger()

if __name__ == "__main__":
    DogDodgerApp().run()
