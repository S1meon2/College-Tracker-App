from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder


# Define the screens in KV
AppUI = '''
ScreenManager:
    MainScreen:
    SettingsScreen:
    ClassAddScreen:
    SignInScreen:
<MainScreen>:
    name: "main"

    MDRaisedButton:
        text: "Sign In"
        pos_hint: {"top": 0.98, "right": 0.11}
        on_release: root.manager.current = "sign in"

    MDRaisedButton:
        text: "Settings"
        pos_hint: {"top": 0.98, "right": 0.98}
        # This is the magic line that switches screens
        on_release: root.manager.current = "settings"

    MDRaisedButton:
        text: "Add Class"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        on_release: root.manager.current = "add a class"

<SettingsScreen>:
    name: "settings"

    MDLabel:
        text: "Settings Page"
        halign: "center"

    MDRaisedButton:
        text: "Back to Home"
        pos_hint: {"center_x": 0.5, "center_y": 0.4}
        on_release: root.manager.current = "main"
        
    MDRaisedButton:
        text: "Connect Zybooks"
        pos_hint: {"center_x": 0.5, "center_y": 0.8}
        
    MDRaisedButton:
        text: "Connect Cengage"
        pos_hint: {"center_x": 0.5, "center_y": 0.7}
        
    MDRaisedButton:
        text: "Connect Blackboard"
        pos_hint: {"center_x": 0.5, "center_y": 0.6}
        
    MDRaisedButton:
        text: "Connect Google"
        pos_hint: {"center_x": 0.5, "center_y": 0.2}
        
    MDRaisedButton:
        text: "Auto-Update ON"
        pos_hint: {"center_x": 0.1, "center_y": 0.1}
        
    MDRaisedButton:
        text: "Update"
        pos_hint: {"center_x": 0.9, "center_y": 0.1}

        
<ClassAddScreen>:
    name: "add a class"
    
    MDLabel:
        text: "+ ADD a class!"
        halign: "center"
        
    MDRaisedButton:
        text: "Back to Home"
        pos_hint: {"center_x": 0.5, "center_y": 0.4}
        on_release: root.manager.current = "main"
        
<SignInScreen>:
    name: "sign in"
    
    MDLabel:
        text: "create username: "
        halign: "left"
        valign: "top"
        
    MDLabel:
        text: "create pin number:"
        halign: "right"
        valign: "top"
        
    MDRaisedButton:
        text: "Back to Home"
        pos_hint: {"center_x": 0.5, "center_y": 0.4}
        on_release: root.manager.current = "main"
'''


# We need these empty classes so Python recognizes the KV tags
class MainScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class ClassAddScreen(Screen):
    pass

class SignInScreen(Screen):
    pass

class UBubbleApp(MDApp):
    def build(self):
        return Builder.load_string(AppUI)


if __name__ == "__main__":
    UBubbleApp().run()