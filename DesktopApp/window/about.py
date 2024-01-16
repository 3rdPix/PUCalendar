# coding:utf-8
import sys

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtGui import QPixmap, QImage

from qfluentwidgets import (PushButton, TeachingTip, TeachingTipTailPosition, InfoBarIcon, setTheme, Theme,
                            TeachingTipView, FlyoutViewBase, BodyLabel, PrimaryPushButton, PopupTeachingTip, FluentIcon as FIF)


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet("Demo{background: rgb(32, 32, 32)}")

        self.hBoxLayout = QHBoxLayout(self)
        self.button1 = PushButton('Top', self)

        self.resize(700, 500)
        self.button1.setFixedWidth(150)
        self.hBoxLayout.addWidget(self.button1, 0, Qt.AlignmentFlag.AlignHCenter)
        self.button1.clicked.connect(self.showTopTip)

    def showTopTip(self):
        position = TeachingTipTailPosition.LEFT_BOTTOM
        imagen = QPixmap('../assets/campus.jpg')
        view = TeachingTipView(
            icon=None,
            title='Información de la aplicación',
            content="PUCalendar es una aplicación diseñada para \
estudiantes con la finalidad de ayudar en el registro y organización de todas \
las actividades que la universidad y sus cursos ofrecen durante el semestre.\n\
Este calendario de código abierto es diseñado por y para alumnos.",
            image=imagen,
            isClosable=True,
            tailPosition=position,
        )

        # add widget to view
        button = PushButton(FIF.GITHUB, 'GitHub')
        view.addWidget(button, align=Qt.AlignmentFlag.AlignRight)

        tip = TeachingTip.make(
            view, target=self.button1, duration=-1, tailPosition=position, parent=self)
        view.closed.connect(tip.close)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()