import kivy
import os
from kivy.clock import Clock
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
    wpm_text = ObjectProperty(None)
    play_button = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(Root, self).__init__(*args, **kwargs)
        self.wpm = 250
        self.text_event = None
        self.text = None
        self.curr_word = 0
        self.playing = False
        self.wpm_text.bind(text=self.wpm_updated)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = FileLoader(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            new_text = stream.read()
            self.text = new_text.split()
            if len(self.text) > 0:
                self.curr_word = 0
                self.label.text = self.text[0]
                self.update_timer()
        self.dismiss_popup()

    def toggle_play(self):
        if self.text and self.curr_word >= len(self.text) - 1:
            self.curr_word = 0
        self.playing = not self.playing
        self.play_button.text = "Pause" if self.playing else "Play"
        self.update_timer()

    def wpm_updated(self, _, text):
        if text:
            self.wpm = int(text)
            self.update_timer()

    def update_timer(self):
        if self.text_event is not None:
            self.text_event.cancel()
        if self.wpm > 0 and self.playing:
            self.text_event = Clock.schedule_interval(lambda dt: self.update_text(), 60.0 / self.wpm)

    def update_text(self):
        if self.text is not None:
            if self.curr_word >= len(self.text):
                self.toggle_play()
                return
            self.label.text = self.text[self.curr_word]
            self.curr_word += 1
        else:
            self.toggle_play()

# Create the App class
class MarlinApp(App):
    def build(self):
        return Root()


if __name__ == '__main__':
    MarlinApp().run()
