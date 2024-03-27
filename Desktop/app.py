import json
import sys
from enum import Enum
from os.path import join
from typing import List

from PyQt6 import QtMultimedia
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QHBoxLayout
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import MessageBox
from qfluentwidgets import MSFluentWindow
from qfluentwidgets import NavigationAvatarWidget
from qfluentwidgets import NavigationItemPosition
from qfluentwidgets import PushButton
from qfluentwidgets import qrouter
from qfluentwidgets import setFont
from qfluentwidgets import setTheme
from qfluentwidgets import SubtitleLabel
from qfluentwidgets import TeachingTip
from qfluentwidgets import TeachingTipTailPosition
from qfluentwidgets import TeachingTipView
from qfluentwidgets import Theme

from components.main_logic import MainLogic
from components.paths import Paths
from components.text import AppText
from window.home import HomeInterface
from window.main_window import MainWindow

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

        # self.connect_signals()

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

    def connect_signals(self) -> None:
        
        # newclass creation search query
        self.mainWindow.courses_interface.newclass_search_interface.do_search.connect(
            self.logic.newclass_search)
        
        # newclass creation search result
        self.logic.search_result.connect(
            self.mainWindow.courses_interface.newclass_search_interface.show_search_result)

        # newclass selection
        self.mainWindow.courses_interface.newclass_search_interface.newclass_fromWeb.connect(
            self.logic.newclass_fromWeb)
        open()
        # newclass show DANGER
        self.logic.toFront_loadCourse.connect(
            self.mainWindow.courses_interface.add_new)
