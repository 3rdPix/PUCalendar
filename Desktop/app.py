import sys
from typing import List

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QDesktopServices, QPixmap
from PyQt6.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import (TeachingTip, PushButton, TeachingTipView, TeachingTipTailPosition, NavigationItemPosition, MessageBox, setTheme, Theme, MSFluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont)
from qfluentwidgets import FluentIcon as FIF
from window.home import HomeInterface
from typing import List
import json
from enum import Enum
from os.path import join
from components.paths import Paths
from components.text import AppText
from window.main_window import MainWindow
from components.main_logic import MainLogic

class PUCalendar(QApplication):
    """
    Calendar App
    """

    def __init__(self, argv: List[str]) -> None:
        super().__init__(argv)

        # Load paths, resources and files
        Paths.load_paths('paths.json')
        AppText.load_text(Paths.get('text'))
        self.logic = MainLogic()
        self.logic.initSession()
        self.logic.printCourses()
        self.mainWindow = MainWindow()
        self.mainWindow.show()

