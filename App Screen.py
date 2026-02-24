from kivymd.app import MDApp
from kivy.lang import Builder

# First Page Visuals
First_Page = '''
MDScreen:
    MDRaisedButton:
        text: "Sign In"
        pos_hint: {"top": 0.98, "right": 0.11}
        
    MDRaisedButton:
        text: "Settings"
        pos_hint: {"top": 0.98, "right": 0.98}
        
    MDRaisedButton:
        text: "Add Class"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: (0.4, 0.1)
    
'''

#Load first page
class UBubbleApp(MDApp):
    def build(self):
        return Builder.load_string(First_Page)

# Run
if __name__ == "__main__":
    UBubbleApp().run()