from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from workoutbanner import WorkoutBanner
import requests
import json


class HomeScreen(Screen):
    pass


class ImageButton(ButtonBehavior, Image):
    pass


class SettingsScreen(Screen):
    pass


GUI = Builder.load_file("main.kv")


class MainApp(App):
    my_friend_id = 1

    def build(self):
        return GUI

    def on_start(self):
        result = requests.get(f"https://friendly-fitness-app-6a322.firebaseio.com/{self.my_friend_id}.json")
        data = json.loads(result.content.decode())

        avatar_image = self.root.ids["avatar_image"]
        avatar_image.source = f"icons/avatars/{data['avatar']}"

        streak_label = self.root.ids["home_screen"].ids["streak_label"]
        streak_label.text = str(data["streak"]) + " Day Streak!"

        friend_id_label = self.root.ids["settings_screen"].ids["friend_id_label"]
        friend_id_label.text = "Friend ID: " + str(self.my_friend_id)

        banner_grid = self.root.ids["home_screen"].ids["banner_grid"]
        workouts = data["workouts"][1:]
        for workout in workouts:
            for i in range(5):
                W = WorkoutBanner(
                    workout_image=workout['workout_image'], 
                    description=workout['description'], 
                    type_image=workout['type_image'], 
                    number=workout['number'], 
                    units=workout['units'], 
                    likes=workout['likes'])
                banner_grid.add_widget(W)

    def change_screen(self, screen_name):
        screen_manager = self.root.ids["screen_manager"]
        screen_manager.current = screen_name


MainApp().run()
