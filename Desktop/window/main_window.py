import sys
from enum import Enum
from typing import List

from components.paths import Paths
from components.text import AppText
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QKeyEvent
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
from window import AgendaInterface
from window import CalendarTab
from window import MyPUClassesTab
from window.home import HomeInterface

class MainWindow(MSFluentWindow):

    __showing_about: bool = False

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.init_window()
        self.init_contents()
        self.init_navigation()


    def init_window(self) -> None:
        self.resize(750, 750)
        self.setWindowIcon(QIcon(Paths.get('window_icon')))
        self.setWindowTitle('PUCalendar')
        with open(Paths.get('qss'), mode='r', encoding='utf-8') as style:
            self.setStyleSheet(style.read())
        
    def init_contents(self) -> None:
        self.home_interface = HomeInterface(self)
        self.agenda_interface = AgendaInterface('Agenda', self)
        self.courses_interface = MyPUClassesTab(self)
        self.calendar_interface = CalendarTab('Calendario', self)

    def init_navigation(self) -> None:
        self.addSubInterface(self.home_interface, FIF.HOME, 'Inicio', FIF.HOME_FILL)
        self.addSubInterface(self.agenda_interface, FIF.TAG, 'Agenda', FIF.CHECKBOX)
        self.addSubInterface(self.courses_interface, FIF.LIBRARY, 'Cursos', FIF.LIBRARY_FILL)
        self.addSubInterface(self.calendar_interface, FIF.CALENDAR, 'Calendario')

        self.navigationInterface.addItem(
            routeKey='aboutapp', icon=FIF.HELP, text='Acerca de',
            onClick=self.show_about_bubble, selectable=False,
            position=NavigationItemPosition.BOTTOM)
        
    def show_about_bubble(self) -> None:
        if self.__showing_about: return
        self.__showing_about = True
        tail_position = TeachingTipTailPosition.LEFT_BOTTOM
        image = QPixmap(Paths.get('about_background'))
        bubble = TeachingTipView(title=AppText.APP_DESCRIPTION_TITLE,
                                 content=AppText.APP_DESCRIPTION, image=image,
                                 isClosable=True, tailPosition=tail_position)
        github_button = PushButton(FIF.GITHUB, 'GitHub')
        bubble.addWidget(github_button, align=Qt.AlignmentFlag.AlignRight)
        panel = TeachingTip.make(bubble, self.navigationInterface, 
                                 duration=-1, tailPosition=tail_position,
                                 parent=self)
        
        bubble.closed.connect(lambda: self.hide_about_bubble(panel))
    
    def hide_about_bubble(self, panel: TeachingTip) -> None:
        panel.close()
        self.__showing_about = False
