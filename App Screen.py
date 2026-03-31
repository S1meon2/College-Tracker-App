from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen

# We need these empty classes so Python recognizes the KV tags
class MainScreen(Screen): pass
class SettingsScreen(Screen):
    def enter_zybooks(self):
        websiteName = "zybooks"
class ClassAddScreen(Screen): pass
class SignInScreen(Screen): pass
class WebsiteDataScreen(Screen):
    def save_input(self):
        user_name = self.ids.username_field.text
        user_pass = self.ids.password_field.text


# Build and Modify the app
class UBubbleApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.theme_style = "Dark"
        return

# Run
if __name__ == "__main__":
    UBubbleApp().run()

