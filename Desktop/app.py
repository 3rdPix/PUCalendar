from typing import List
from PyQt6 import QtMultimedia
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication
from components.main_logic import MainLogic
from components.paths import Paths
from components.text import AppText
from window import MainWindow

class PUCalendar(QApplication):
    """
    Calendar App
    """

    def __init__(self, argv: List[str]) -> None:
        super().__init__(argv)

        # Load paths, resources and files
        Paths.load_paths('paths.json')
        AppText.load_text(Paths.get('text'))
        
        # application handler
        self.logic = MainLogic()
        
        # window
        self.mainWindow = MainWindow()

        self.connect_courses_tab_signals()

        # self.init_game_music()
        self.mainWindow.show()

    def init_game_music(self) -> None:
        self.audio_output: QtMultimedia.QAudioOutput = \
            QtMultimedia.QAudioOutput()
        self.audio_output.setVolume(0.2)
        self.music_player: QtMultimedia.QMediaPlayer = \
            QtMultimedia.QMediaPlayer(self)
        self.music_player.setAudioOutput(self.audio_output)
        self.music_player.setSource(QUrl.fromLocalFile('gains.mp3'))
        self.music_player.play()

    def connect_courses_tab_signals(self) -> None:
        
        # search for puclass
        self.mainWindow.courses_interface.SGsearch_for_puclass.connect(
            self.logic.RQsearch_for_puclass)
        
        # send search results
        self.logic.SG_CourT_search_result.connect(
            self.mainWindow.courses_interface.show_search_results)
        
        # send newclass selection
        self.mainWindow.courses_interface.SGselect_newclass.connect(
            self.logic.RQcreate_new_puclass)
        
        # receive creation
        self.logic.SG_CourT_add_card_to_allpuclass_panel.connect(
            self.mainWindow.courses_interface.add_new)

        # infobox clicked
        self.mainWindow.courses_interface.SGpuclass_clicked.connect(
            self.logic.RQpuclass_clicked)
        
        # puclass panel info
        self.logic.SG_CourT_show_single_puclass_panel.connect(
            self.mainWindow.courses_interface.show_puclass_panel)