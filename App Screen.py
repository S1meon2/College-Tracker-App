from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from dataclasses import dataclass
from Assignment_WEB import scrape_cengage, scrape_zybooks, scrape_blackboard
from ububbleDB import send_info, recieve_info

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
    def update(self):
        recieve_info()


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
    def print_assignments(self):
        if MDApp.get_running_app().classWeb == "cengage":
            scrape_cengage(MDApp.get_running_app().cengageSN.name, MDApp.get_running_app().cengageSN.username, MDApp.get_running_app().cengageSN.password)
        if MDApp.get_running_app().classWeb == "zybooks":
            scrape_zybooks(MDApp.get_running_app().zybooksSN.name, MDApp.get_running_app().zybooksSN.username, MDApp.get_running_app().zybooksSN.password)
        if MDApp.get_running_app().classWeb == "blackboard":
            scrape_blackboard(MDApp.get_running_app().blackboardSN.name, MDApp.get_running_app().blackboardSN.username, MDApp.get_running_app().blackboardSN.password)



class SignInScreen(Screen): pass
class WebsiteDataScreen(Screen):
    def save_input(self):
        MDApp.get_running_app().user_name = self.ids.username_field.text
        MDApp.get_running_app().user_pass = self.ids.password_field.text
    def save_data(self):
        if MDApp.get_running_app().websiteName == "cengage":
            MDApp.get_running_app().cengageSN = WebsiteSN(name=MDApp.get_running_app().websiteName, username=MDApp.get_running_app().user_name, password=MDApp.get_running_app().user_pass)
            send_info(MDApp.get_running_app().cengageSN.name, MDApp.get_running_app().cengageSN.username,MDApp.get_running_app().cengageSN.password)
            print(MDApp.get_running_app().cengageSN)
        if MDApp.get_running_app().websiteName == "zybooks":
            MDApp.get_running_app().zybooksSN = WebsiteSN(name=MDApp.get_running_app().websiteName, username=MDApp.get_running_app().user_name, password=MDApp.get_running_app().user_pass)
            send_info(MDApp.get_running_app().zybooksSN.name, MDApp.get_running_app().zybooksSN.username,MDApp.get_running_app().zybooksSN.password)
            print(MDApp.get_running_app().zybooksSN)
        if MDApp.get_running_app().websiteName == "blackboard":
            MDApp.get_running_app().blackboardSN = WebsiteSN(name=MDApp.get_running_app().websiteName, username=MDApp.get_running_app().user_name, password=MDApp.get_running_app().user_pass)
            send_info(MDApp.get_running_app().blackboardSN.name, MDApp.get_running_app().blackboardSN.username,MDApp.get_running_app().blackboardSN.password)
            print(MDApp.get_running_app().blackboardSN)



# Build and Modify the app
class UBubbleApp(MDApp):
    classID = ""
    className = ""
    classWeb = ""
    websiteName = ""
    user_name = ""
    user_pass = ""
    zybooksSN = ""
    cengageSN = ""
    blackboardSN = ""

    def build(self):
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.theme_style = "Dark"
        return


# Run
if __name__ == "__main__":
    UBubbleApp().run()

