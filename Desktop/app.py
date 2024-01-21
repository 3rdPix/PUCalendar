import sys

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QIcon, QDesktopServices, QPixmap
from PyQt6.QtWidgets import QApplication, QFrame, QHBoxLayout
from qfluentwidgets import (TeachingTip, PushButton, TeachingTipView, TeachingTipTailPosition, NavigationItemPosition, MessageBox, setTheme, Theme, MSFluentWindow,
                            NavigationAvatarWidget, qrouter, SubtitleLabel, setFont)
from qfluentwidgets import FluentIcon as FIF
from window.inicio import InterfazInicio


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))



class VentanaPrincipal(MSFluentWindow):

    def __init__(self):
        super().__init__()

        # Crear sub interfaces
        self.InterfazInicio = InterfazInicio(parent=self)
        self.InterfazCalendario = Widget('Calendario', self)
        self.InterfazDeberes = Widget('Actividades pendientes', self)
        self.InterfazCursos = Widget('Cursos', self)
        self.InterfazConfiguracion = Widget('Configuraciones', self)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.InterfazInicio, FIF.HOME, 'Inicio', FIF.HOME_FILL)
        self.addSubInterface(self.InterfazCalendario, FIF.CALENDAR, 'Calendario')
        self.addSubInterface(self.InterfazDeberes, FIF.CHECKBOX, 'Pendientes')
        self.addSubInterface(self.InterfazCursos, FIF.BOOK_SHELF, 'Cursos')

        self.addSubInterface(self.InterfazConfiguracion, FIF.SETTING, 'Configuraciones', position=NavigationItemPosition.BOTTOM)
        self.navigationInterface.addItem(
            routeKey='Help',
            icon=FIF.HELP,
            text='Acerca de',
            onClick=self.mostrarAcercade,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.setCurrentItem(self.InterfazInicio.objectName())

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon('assets/uc.png'))
        self.setWindowTitle('PUCalendar')
        

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        with open('resource/qss/window.qss', mode='r', encoding='utf-8') as style:
            self.setStyleSheet(style.read())

    def mostrarAcercade(self):
        posicion_cola = TeachingTipTailPosition.LEFT_BOTTOM
        imagen = QPixmap('assets/campus.jpg')
        visualizador = TeachingTipView(
            title='Información de la aplicación',
            content="\
PUCalendar es una aplicación de código abierto\n\
diseñada por y para estudiantes con la finalidad\n\
de otorgar una ayuda en la organización y registro\n\
de todos los quehaceres universitarios.",
            image=imagen,
            isClosable=True,
            tailPosition=posicion_cola)
        
        boton_github = PushButton(FIF.GITHUB, 'GitHub')
        visualizador.addWidget(boton_github, align=Qt.AlignmentFlag.AlignRight)
        burbuja = TeachingTip.make(visualizador, target=self.navigationInterface,
                                    duration=-1, tailPosition=posicion_cola, parent=self)
        visualizador.closed.connect(burbuja.close)


if __name__ == '__main__':
    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = VentanaPrincipal()
    w.show()
    app.exec()
