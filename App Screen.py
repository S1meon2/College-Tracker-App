from kivy.app import App
from kivy.uix.label import Label

# MyApp(App)
class MyApp(App):
    def build(self):
        return Label(text="Welcome to U-Bubble!")



# Run
if __name__ == '__main__':
    MyApp().run()
