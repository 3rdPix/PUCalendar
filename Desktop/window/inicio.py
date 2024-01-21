from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QGridLayout
from PyQt6.QtGui import QPaintEvent, QPixmap, QPainter, QLinearGradient, QColor, QBrush, QPainterPath, QResizeEvent
from PyQt6.QtCore import Qt, QRectF
from qfluentwidgets import isDarkTheme, ScrollArea, FlowLayout, SubtitleLabel, SmoothScrollArea
from components.summary_box import InfoBox


class InterfazInicio(QFrame):
    """Contenedor superior"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('Inicio')

        self.init_contenido()
        inner_layout = FlowLayout(needAni=True)
        inner_layout.addWidget(self.iBAgenda)
        inner_layout.addWidget(self.iBCursos)
        inner_layout.addWidget(self.iBPeligro)
        inner_layout.addWidget(self.iBConfiguraciones)

        # test
        inner_layout.addWidget(self.iba)
        inner_layout.addWidget(self.ibb)
        inner_layout.addWidget(self.ibc)
        inner_layout.addWidget(self.ibd)
        inner_layout.addWidget(self.ibe)
        inner_layout.addWidget(self.ibf)
        inner_layout.addWidget(self.ibg)
        inner_layout.addWidget(self.ibh)
        

        self.area = ScrollArea(self)
        self.transition = QWidget()
        self.area.setWidget(self.transition)
        self.area.setWidgetResizable(True)
        self.transition.setLayout(inner_layout)

        contenedor = QGridLayout()
        contenedor.addWidget(self.transition)
        self.setLayout(contenedor)


    def init_contenido(self) -> None:
        self.iBAgenda           = InfoBox('Próximas actividades')
        self.iBCursos           = InfoBox('Progreso ramos')
        self.iBPeligro          = InfoBox('Ramos en peligro')
        self.iBConfiguraciones  = InfoBox('Configuraciones')

        # test
        self.iba = InfoBox('algo')
        self.ibb = InfoBox('B')
        self.ibc = InfoBox('C')
        self.ibd = InfoBox('D')
        self.ibe = InfoBox('E')
        self.ibf = InfoBox('F')
        self.ibg = InfoBox('G')
        self.ibh = InfoBox('H')