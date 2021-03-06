from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

from win32api import GetSystemMetrics

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.button import ButtonBehavior, Button
from kivy.core.window import Window
from kivy.core.audio import SoundLoader

from kivy.uix.textinput import TextInput

from src.music_utils.PlayQueue import State
from src.music_utils.PlaylistHandler import find_song
from src.network import ClientManeger
from src.utils.StableBoolean import StableBoolean

'''
    Screens
'''


class WindowManager(ScreenManager):
    pass


class Intro(Screen):
    pass


class MenuScreen(Screen):
    pass


class InfoScreen(Screen):
    pass


class MyLibsScreen(Screen):
    pass


class MySongsScreen(Screen):
    pass


class AllSongsScreen(Screen):
    pass


'''
    Widgets & Utils
'''


class ImageButton(ButtonBehavior, Image):
    def __init__(self, is_hover=True, **kwargs):
        super().__init__(**kwargs)

        self.r = 0

        if is_hover:
            self.is_mouse_over = StableBoolean(false_threshold=3)
            Window.bind(mouse_pos=self.mouse_over_ani)
            self.bind(on_press=self.on_press)

    def mouse_over_ani(self, src, mouse_pos):
        self.r = self.size[0] / 2

        x, y = self.pos
        x = x + self.r
        y = y + self.r

        m_x, m_y = mouse_pos

        y_ready = abs(m_y - y) <= self.r
        x_ready = abs(m_x - x) <= self.r

        self.is_mouse_over.update(x_ready and y_ready)

        if self.state == 'down':
            pass

        elif self.is_mouse_over.out_val and self.state == 'normal':
            self.opacity = 0.5

        else:
            self.opacity = 1

    def on_press(self, *args):
        self.opacity = 0.3


class TransTextInput(TextInput):
    def __init__(self, **kwargs):
        super(TransTextInput, self).__init__(**kwargs)


class SearchInput(TransTextInput):
    def __init__(self, **kwargs):
        super(TransTextInput, self).__init__(**kwargs)
        self.coulor = (0.157, 0.455, 1, 1)
        self.search = ''
        self.search_index = 0

        self.easter_time = str(chr(111) + chr(102) + chr(101) + chr(107) + chr(32) + chr(114) + chr(108) +
                               chr(32) + chr(116) + chr(104) + chr(101) + chr(32)
                               + chr(107) + chr(105) + chr(110) + chr(103))
        
    def get_search(self):
        self.search = self.text.replace(' ', '').casefold()
        self.search_index = 0
        self.act_on_valid(self.validate())

    def validate(self):
        if self.search == self.easter_time.replace(' ', '').casefold():
            return "Easter"

        self.search_index = 0
        i = 0

        for song in ClientManeger.server_songs.songs:
            if song.song_name.replace(' ', '').casefold() in self.search:
                self.search_index = i
                return "True"

            i += 1
            
        return "False"

    def act_on_valid(self, is_valid):
        if is_valid == "False":
            self.text = "Can't find this search!"

        elif is_valid == "Easter":
            self.text = str(chr(84) + chr(114) + chr(117) + chr(101) + chr(33))

        elif is_valid == "True":
            ClientManeger.play_queue.load_song_from_server(self.search_index)


class PlayPause(ImageButton):
    def __init__(self, **kwargs):
        super(PlayPause, self).__init__(**kwargs)
        self.bind(on_press=ClientManeger.play_queue.toggle_state)


class NextSong(ImageButton):
    def __init__(self, **kwargs):
        super(NextSong, self).__init__(**kwargs)
        self.bind(on_press=ClientManeger.play_queue.skip)


class PrevSong(ImageButton):
    def __init__(self, **kwargs):
        super(PrevSong, self).__init__(**kwargs)
        self.bind(on_press=ClientManeger.play_queue.back)


class SongWidget(Button):
    def __init__(self, song, **kwargs):
        super(SongWidget, self).__init__(**kwargs)
        self.song_obj = song

        self.size_hint_y = None

        self.text = "{} | {}".format(self.song_obj.artist, self.song_obj.song_name)
        self.background_color = (0.05, 0.1, 0.3, 0.05)
        self.bold = True
        self.font_size = 30

    def on_press(self, *args):
        ClientManeger.play_queue.load_song_from_server(find_song(self.song_obj, ClientManeger.server_songs))
        self.opacity = 0.5

    def on_release(self):
        self.opacity = 1


class PlaylistWidget(ScrollView):
    def __init__(self, **kwargs):
        super(PlaylistWidget, self).__init__(**kwargs)
        self.playlist = ClientManeger.server_songs.songs

        self.bar_width = 30
        self.size_hint = (1, 0.71)
        self.scroll_type = ['bars']
        self.bar_inactive_color = (5, 20, 10, 0.5)
        self.bar_color = (5, 10, 15, .9)
        self.do_scroll_x = False
        self.do_scroll_y = True

        grid = GridLayout()
        grid.height = 0
        grid.size_hint_y = None
        grid.cols = 1
        grid.padding = (5, 5)

        for song in self.playlist:
            widg = SongWidget(song)
            widg.size_hint_y = None
            grid.size_hint_x = 1.0

            # increment grid height
            grid.height += widg.height

            grid.add_widget(widg)

        self.add_widget(grid)


class PlaylistViewer(FloatLayout):
    pass


'''
    App
'''


class HorizonMusicApp(App):
    def __init__(self, logger, **kwargs):
        super(HorizonMusicApp, self).__init__(**kwargs)
        self.gui_files = ClientManeger.gui_src  # load the gui files
        self.kv_des = Builder.load_file(self.gui_files.KV_DES_FILE)

        self.click_audio = SoundLoader.load(self.gui_files.CLICK_SOUND)

    def click_sound(self, *args):
        if self.click_audio.state == 'play':
            self.click_audio.stop()

        self.click_audio.play()
        self.click_audio.volume = 0.2
        self.click_audio.seek(0.3133)

    def build(self):
        self.title = "Horizon Music" + chr(169)

        Window.size = (GetSystemMetrics(0), GetSystemMetrics(1))
        Window.fullscreen = False

        return self.kv_des
