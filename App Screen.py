from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen

# We need these empty classes so Python recognizes the KV tags
class MainScreen(Screen): pass
class SettingsScreen(Screen): pass
class ClassAddScreen(Screen): pass
class SignInScreen(Screen): pass

# Build and Modify the app
class UBubbleApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"
        return

# Run
if __name__ == "__main__":
    UBubbleApp().run()