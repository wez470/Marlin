import kivy
import os
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.app import App
kivy.require('1.11.0')


class FileLoader(BoxLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(GridLayout):
    label = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = FileLoader(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.label.text = stream.read()

        self.dismiss_popup()


# Create the App class
class MarlinApp(App):
    def build(self):
        return Root()


if __name__ == '__main__':
    MarlinApp().run()
