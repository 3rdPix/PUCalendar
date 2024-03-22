import sys
from typing import List

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QDesktopServices, QKeyEvent, QPixmap
from PyQt6.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import (TeachingTip, PushButton, TeachingTipView, TeachingTipTailPosition, NavigationItemPosition, MessageBox, setTheme, Theme, MSFluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont)
from qfluentwidgets import FluentIcon as FIF
from window.home import HomeInterface
from typing import List
from enum import Enum
from components.paths import Paths
from components.text import AppText
from window import AgendaInterface, CoursesInterface, CalendarInterface

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
        self.courses_interface = CoursesInterface('Cursos', self)
        self.calendar_interface = CalendarInterface('Calendario', self)

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

    def keyPressEvent(self, a0: QKeyEvent | None) -> None:
        self.courses_interface.keyPressEvent(a0)
        return super().keyPressEvent(a0)