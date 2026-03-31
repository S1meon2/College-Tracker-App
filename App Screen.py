from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from dataclasses import dataclass

#Use below to make gobal variables
"""MDApp.get_running_app()."""

#Website Sign-ins
@dataclass
class WebsiteSN:
    name: str
    username: str
    password: str

#Class Adding
@dataclass
class Course:
    name: str
    website: str
    id: str

# We need these empty classes so Python recognizes the KV tags
class MainScreen(Screen): pass
class SettingsScreen(Screen):
    def enter_zybooks(self):
        MDApp.get_running_app().websiteName = "zybooks"
    def enter_cengage(self):
        MDApp.get_running_app().websiteName = "cengage"
    def enter_blackboard(self):
        MDApp.get_running_app().websiteName = "blackboard"
class ClassAddScreen(Screen):
    def enter_className(self):
        MDApp.get_running_app().className = self.ids.class_name.text
    def enter_classWeb(self):
        MDApp.get_running_app().classWeb = self.ids.assignment_website.text
    def enter_classID(self):
        MDApp.get_running_app().classID = self.ids.class_identifier.text
    def save_data(self):
        courseData = Course(name=MDApp.get_running_app().className, website=MDApp.get_running_app().classWeb, id=MDApp.get_running_app().classID)
        print(courseData)
class SignInScreen(Screen): pass
class WebsiteDataScreen(Screen):
    def save_input(self):
        MDApp.get_running_app().user_name = self.ids.username_field.text
        MDApp.get_running_app().user_pass = self.ids.password_field.text
    def save_data(self):
        zybooksSN = WebsiteSN(name=MDApp.get_running_app().websiteName, username=MDApp.get_running_app().user_name, password=MDApp.get_running_app().user_pass)
        print(zybooksSN)



# Build and Modify the app
class UBubbleApp(MDApp):
    classID = ""
    className = ""
    classWeb = ""
    websiteName = ""
    user_name = ""
    user_pass = ""

    def build(self):
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.theme_style = "Dark"
        return

# Run
if __name__ == "__main__":
    UBubbleApp().run()

