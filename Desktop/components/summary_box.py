from PyQt6.QtCore import Qt
from qfluentwidgets import SubtitleLabel, ToolButton, FluentIcon as FIF, PrimaryToolButton
from PyQt6.QtWidgets import QFrame, QWidget, QVBoxLayout, QHBoxLayout

class InfoBox(QFrame):

    def __init__(self, titulo_seccion: str, parent: QWidget=None) -> None:
        super().__init__(parent)
        self.setFixedSize(250, 270)
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Plain)
        self.titulo = SubtitleLabel(text=titulo_seccion, parent=self)
        self.boton_redirigir = PrimaryToolButton(FIF.RIGHT_ARROW, parent=self)
        self.contenido = QFrame(parent=self)
        texto = SubtitleLabel(text='contenido', parent=self.contenido)
        texto.setAlignment(Qt.AlignmentFlag.AlignCenter)

        verticalbox = QVBoxLayout()
        horizontal = QHBoxLayout()
        horizontal.addWidget(self.titulo)
        horizontal.addWidget(self.boton_redirigir)
        verticalbox.addLayout(horizontal)
        verticalbox.addWidget(self.contenido)
        self.setLayout(verticalbox)