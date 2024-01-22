from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QGridLayout
from PyQt6.QtGui import QPaintEvent, QPixmap, QPainter, QLinearGradient, QColor, QBrush, QPainterPath, QResizeEvent
from PyQt6.QtCore import Qt, QRectF
from qfluentwidgets import isDarkTheme, ScrollArea, FlowLayout, SubtitleLabel, SmoothScrollArea
from components.summary_box import InfoBox


class HomeInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('home')
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)


        self.widget_object = QWidget(parent=self)
        self.flow_layout = FlowLayout(parent=self.widget_object, needAni=True)
        

        self.init_content()
        self.flow_layout.addWidget(self.iBAgenda)
        self.flow_layout.addWidget(self.iBCursos)
        self.flow_layout.addWidget(self.iBConfiguraciones)
        self.flow_layout.addWidget(self.iBPeligro)
        self.flow_layout.addWidget(self.iBExternal)

        self.setWidget(self.widget_object)

    def init_content(self) -> None:
        self.iBAgenda           = InfoBox('Próximas actividades')
        self.iBCursos           = InfoBox('Progreso ramos')
        self.iBPeligro          = InfoBox('Ramos en peligro')
        self.iBConfiguraciones  = InfoBox('Configuraciones')
        self.iBExternal         = InfoBox('Enlaces externos')
