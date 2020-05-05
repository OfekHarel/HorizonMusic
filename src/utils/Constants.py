from pathlib import Path

class GUIFiles:
    def __init__(self):
        self.GUI_PATH = str(Path.cwd() / 'ui')

        self.KV_DES_FILE = self.GUI_PATH + r'\design\horizon_music_des.kv'
        self.CLICK_SOUND = self.GUI_PATH + r'\sounds\click.mp3'
        self.BACKGROUND = self.GUI_PATH + r'\images\screens\BackG.png'
        self.INFO_SCREEN = self.GUI_PATH + r'\images\screens\info.png'
        self.BACKWARD_WINDOW_WIDGET = self.GUI_PATH + r'\images\widgets\Backw.png'
        self.CONTINUE_WINDOW_WIDGET = self.GUI_PATH + r'\images\widgets\cont.png'
        self.BACK_TO_MENU_WIDGET = self.GUI_PATH + r'\images\widgets\BtoM.png'
        self.INFO_WIDGET = self.GUI_PATH + r'\images\widgets\Info.png'
        self.ALL_MUSIC_WIDGET = self.GUI_PATH + r'\images\widgets\Music.png'
        self.FOLDER_WIDGET = self.GUI_PATH + r'\images\widgets\Folder.png'
        self.PLAYLIST_WIDGET = self.GUI_PATH + r'\images\widgets\Playlist.png'
        self.QUIT_WIDGET = self.GUI_PATH + r'\images\widgets\Quit.png'
        self.SEARCH_BAR_WIDGET = self.GUI_PATH + r'\images\widgets\SearchBar.png'
        self.SEARCH_WIDGET = self.GUI_PATH + r'\images\widgets\SearchIcon.png'
        self.INTRO = self.GUI_PATH + r'\videos\Intro.avi'


        self.files = [self.KV_DES_FILE, self.CLICK_SOUND, self.BACKGROUND, self.INFO_SCREEN, self.BACKWARD_WINDOW_WIDGET
            , self.BACKWARD_WINDOW_WIDGET, self.BACK_TO_MENU_WIDGET, self.INFO_WIDGET, self.ALL_MUSIC_WIDGET,
                      self.FOLDER_WIDGET
            , self.PLAYLIST_WIDGET, self.QUIT_WIDGET, self.SEARCH_BAR_WIDGET, self.SEARCH_WIDGET, self.INTRO]

        self.is_load = True
        for file in self.files:
            try:
                f = open(file)

            except FileNotFoundError:
                self.is_load = False
                print("ERROR! Can't load file: ", file)

        if self.is_load:
            print("Loaded all GUI files successfully!")


if __name__ == '__main__':
    GUIFiles()
