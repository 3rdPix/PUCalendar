from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout
from PyQt6.QtGui import QPaintEvent, QPixmap, QPainter, QLinearGradient, QColor, QBrush, QPainterPath
from PyQt6.QtCore import Qt, QRectF
from qfluentwidgets import isDarkTheme, ScrollArea, FlowLayout, SubtitleLabel



class InterfazInicio(QFrame):
    """Contenedor superior"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('contenedor')

        area = ScrollArea(self)
        area_layout = FlowLayout(area, True)

        # self.caja1 = CajaResumen('Resumen de pruebas')
        # self.caja2 = CajaResumen('Resumen tareas pendientes')
        # self.caja3 = CajaResumen('Notas pendientes')
        # self.caja4 = CajaResumen('Ramos en peligro')

        # layout.addWidget(self.caja1)
        # layout.addWidget(self.caja2)
        # layout.addWidget(self.caja3)
        # layout.addWidget(self.caja4)

        frame_layout = QHBoxLayout(self)
        frame_layout.addWidget(area)

class CajaResumen(QFrame):
    """Caja con resumen de algún área"""


    def __init__(self, text: str, parent=None) -> None:
        super().__init__(parent)
        self.labelPrueba = SubtitleLabel(text, self)
        self.labelPrueba.setAlignment(Qt.AlignmentFlag.AlignCenter)
        