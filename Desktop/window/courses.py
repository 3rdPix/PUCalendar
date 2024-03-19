from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from qfluentwidgets import SubtitleLabel, setFont, CommandBar, Action, FluentIcon as FIF
from qfluentwidgets.components.widgets.card_widget import CardSeparator


class CoursesInterface(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.command_bar = CommandBar()
        self.command_bar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.command_bar.addAction(Action(FIF.ADD, 'Añadir nuevo'))
        self.command_bar.addAction(Action(FIF.DELETE, 'Eliminar curso'))
        self.command_bar.addAction(Action(FIF.IOT, 'Configurar escala'))

        self.label = SubtitleLabel(text)
        layout = QVBoxLayout(self)
        layout.addWidget(self.command_bar)
        layout.addWidget(CardSeparator())
        layout.addWidget(self.label)

        self.setObjectName(text.replace(' ', '-'))