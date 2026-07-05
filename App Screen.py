from G_Tools import google_auth, sync_assignments_to_tasks
from ububbleDB import send_login, send_class, recieve_scraped
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.animation import Animation
from Assignment_WEB import scrape_cengage, scrape_zybooks, scrape_blackboard, scrape_demo
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.card import MDCard
from kivy.properties import StringProperty, ColorProperty
from kivy.uix.screenmanager import Screen



# Here are the screen's python logic and functions
class MainScreen(Screen):
    pass


class SettingsScreen(Screen):

    def connect_google(self):
        # This will trigger the browser popup to create your token.json
        MDApp.get_running_app().show_notif("Opening browser for Google Authentication...","process")
        google_auth()

    # This helps us know which website the user is choosing to connect
    def choose_website(self, text):
        if text == "blackboard":
            MDApp.get_running_app().websiteName = "blackboard"
        if text == "zybooks":
            MDApp.get_running_app().websiteName = "zybooks"
        if text == "cengage":
            MDApp.get_running_app().websiteName = "cengage"
        if text == "demo":
            MDApp.get_running_app().websiteName = "demo"


class ClassAddScreen(Screen):

    def save_to_class(self):
        classname = self.ids.class_name.text
        webname = self.ids.assignment_website.text
        classid = self.ids.class_identifier.text
        assignmentpage = self.ids.assignment_page_input.text
        send_class(classname, webname, classid, assignmentpage, MDApp.get_running_app().isSignedIn)
        MDApp.get_running_app().show_notif(classname + " has been added and can now be scraped!", "success")

class SignInScreen(Screen):

    def sign_in(self):
        MDApp.get_running_app().isSignedIn = self.ids.username_field.text

class WebsiteDataScreen(Screen):
    def save_to_login(self):
        name = MDApp.get_running_app().websiteName
        userName = self.ids.username_field.text
        userPass = self.ids.password_field.text
        if MDApp.get_running_app().websiteName == "cengage":
            send_login(name, userName, userPass, MDApp.get_running_app().isSignedIn)
            MDApp.get_running_app().show_notif("Cengage connected.","success")
        if MDApp.get_running_app().websiteName == "zybooks":
            send_login(name, userName, userPass, MDApp.get_running_app().isSignedIn)
            MDApp.get_running_app().show_notif("Zybooks connected.","success")
        if MDApp.get_running_app().websiteName == "blackboard":
            send_login(name, userName, userPass, MDApp.get_running_app().isSignedIn)
            MDApp.get_running_app().show_notif("Blackboard connected.","success")
        if MDApp.get_running_app().websiteName == "demo":
            send_login(name, userName, userPass, MDApp.get_running_app().isSignedIn)
            MDApp.get_running_app().show_notif("Demo site connected.","success")


class ClassEditScreen(Screen):
    menu = None  # Define the menu variable

    # on_enter is a Kivy function that runs every time this screen is opened
    def on_enter(self):
        # We only want to build the menu if it hasn't been built yet
        if not self.menu:
            # Right now, these are static. Later, you'll pull these names from ububbleDB.py
            class_names = ["Math", "Computer Science", "English", "Engineering"]

            # Build the list of menu items
            menu_items = [
                {
                    "text": name,
                    "viewclass": "OneLineListItem",
                    # When clicked, pass the name to the set_item function
                    "on_release": lambda x=name: self.set_item(x),
                } for name in class_names
            ]

            # Initialize the dropdown menu
            self.menu = MDDropdownMenu(
                caller=self.ids.class_dropdown_btn,  # Connects to the button ID in your KV file
                items=menu_items,
                width_mult=4,
            )

    def open_menu(self):
        # Open the menu when the button is pressed
        if self.menu:
            self.menu.open()

    def set_item(self, selected_class):
        # Change the button text to show the chosen class
        self.ids.class_dropdown_btn.text = f"Selected: {selected_class}"


        self.menu.dismiss()

        #  Autofill the text field
        self.ids.class_name.text = selected_class

    def enter_className(self):
        MDApp.get_running_app().className = self.ids.class_name.text

    def enter_classWeb(self):
        MDApp.get_running_app().classWeb = self.ids.assignment_website.text

    def enter_classID(self):
        MDApp.get_running_app().classID = self.ids.class_identifier.text

    def print_assignments(self):
        if MDApp.get_running_app().classWeb == "cengage":
            scrape_cengage(MDApp.get_running_app().cengageSN.name, MDApp.get_running_app().cengageSN.username,
                           MDApp.get_running_app().cengageSN.password)
        if MDApp.get_running_app().classWeb == "zybooks":
            scrape_zybooks(MDApp.get_running_app().zybooksSN.name, MDApp.get_running_app().zybooksSN.username,
                           MDApp.get_running_app().zybooksSN.password)
        if MDApp.get_running_app().classWeb == "blackboard":
            scrape_blackboard(MDApp.get_running_app().blackboardSN.name, MDApp.get_running_app().blackboardSN.username,
                              MDApp.get_running_app().blackboardSN.password)

class ClassesScreen(Screen):
    def update_panel(self, class_name, website_name):
        self.ids.class_title.text = class_name
        self.ids.class_website.text = website_name

    def get_assignments_to_tasks(self):
        # 1. Run the scrapers and get the raw text
        print(self.ids.class_website.text)
        raw_text = recieve_scraped(self.ids.class_website.text)

        # 2. Send that text to Gemini and then to Google Tasks
        if raw_text:
            sync_assignments_to_tasks(raw_text)
        else:
            print("No assignments found to sync.")

class TopNotification(MDCard):
    message_text = StringProperty("")
    message_color = ColorProperty([0.7, 0.3, 1, 1])  # Default Purple

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.full_text = ""
        self.char_index = 0
        self.type_event = None

    def show(self, text, notif_type="process"):
        # 1. Set the text color based on the process state
        if notif_type == "error":
            self.message_color = [1, 0.3, 0.3, 1]  # Red
        elif notif_type == "success":
            self.message_color = [0.3, 1, 0.3, 1]  # Green
        else:  # "process"
            self.message_color = [0.7, 0.3, 1, 1]  # Purple

        # 2. Reset text and push the notification off-screen (above the top)
        self.full_text = text
        self.message_text = ""
        self.char_index = 0

        # --- FIX: Change 'y: 1' to 'top: 1.2' ---
        self.pos_hint = {"center_x": 0.5, "top": 1.2}

        # 3. Animate the drop down (this is now mathematically safe!)
        anim = Animation(pos_hint={"center_x": 0.5, "top": 0.96}, duration=0.4, t="out_quad")
        anim.bind(on_complete=self.start_typing)
        anim.start(self)

    def start_typing(self, *args):
        # Cancel any existing typing events to prevent overlapping text
        if self.type_event:
            self.type_event.cancel()

        # Schedule the next character to type every 0.03 seconds
        self.type_event = Clock.schedule_interval(self.type_next_char, 0.03)

    def type_next_char(self, dt):
        if self.char_index < len(self.full_text):
            self.message_text += self.full_text[self.char_index]
            self.char_index += 1
        else:
            self.type_event.cancel()
            # Once fully typed, wait 3 seconds, then trigger the hide animation
            Clock.schedule_once(self.hide, 3)

    def hide(self, dt):
        # --- FIX: Change 'y: 1' to 'top: 1.2' ---
        anim = Animation(pos_hint={"center_x": 0.5, "top": 1.2}, duration=0.4, t="in_quad")
        anim.start(self)

# Build and Modify the app
class UBubbleApp(MDApp):
    #Initialize everything
    classID = className = classWeb = websiteName = user_name = user_pass = zybooksSN = cengageSN = blackboardSN = ""
    isSignedIn = "user"

    def show_notif(self, text, notif_type="process"):
        # This references the notifcation UI in the KV file
        self.root.ids.global_notif.show(text, notif_type)
        #print(text)


    def on_start(self):
        self.show_notif("Welcome to U-Bubble! Sign in to get started.","success")

    def build(self):
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.theme_style = "Dark"
        return


# Run
if __name__ == "__main__":
    UBubbleApp().run()