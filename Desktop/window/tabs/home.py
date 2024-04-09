from PyQt6.QtCore import QEasingCurve
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
from qfluentwidgets import CaptionLabel
from qfluentwidgets import CardWidget
from qfluentwidgets import FlowLayout
from qfluentwidgets import ScrollArea
from qfluentwidgets.components.widgets.card_widget import CardSeparator


class InfoBox(CardWidget):

    def __init__(self, titulo_seccion: str, parent: QWidget=None) -> None:
        super().__init__(parent)
        self.setMinimumSize(170, 200)
        self.titulo = CaptionLabel(titulo_seccion)
        self.separador = CardSeparator()

        lay = QVBoxLayout()
        lay.addWidget(self.titulo)
        lay.addWidget(self.separador)
        self.setLayout(lay)


class HomeInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('home')
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)


        self.widget_object = QWidget(parent=self)
        self.flow_layout = FlowLayout(parent=self.widget_object, needAni=True)
        self.flow_layout.ease = QEasingCurve.Type.InOutExpo

        self.init_content()
        self.flow_layout.addWidget(self.iBAgenda)
        self.flow_layout.addWidget(self.iBCursos)
        self.flow_layout.addWidget(self.iBConfiguraciones)
        self.flow_layout.addWidget(self.iBPeligro)
        self.flow_layout.addWidget(self.iBExternal)
        self.flow_layout.addWidget(self.iBTiempo)

        self.setWidget(self.widget_object)

    def init_content(self) -> None:
        self.iBAgenda           = InfoBox('Próximas actividades')
        self.iBCursos           = InfoBox('Progreso ramos')
        self.iBPeligro          = InfoBox('Ramos en peligro')
        self.iBConfiguraciones  = InfoBox('Configuraciones')
        self.iBExternal         = InfoBox('Enlaces externos')
        self.iBTiempo           = InfoBox('Tiempo dedicado')
