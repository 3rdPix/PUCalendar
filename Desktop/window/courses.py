from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from qfluentwidgets import ScrollArea, SubtitleLabel, setFont, CommandBar, Action, FluentIcon as FIF
from qfluentwidgets.components.widgets.card_widget import CardSeparator
from qfluentwidgets.components.widgets.stacked_widget import OpacityAniStackedWidget
from components.paths import Paths
class CoursesInterface(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.command_bar = CommandBar()
        self.command_bar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.command_bar.addAction(Action(FIF.ADD, 'Añadir nuevo'))
        self.command_bar.addAction(Action(FIF.DELETE, 'Eliminar curso'))
        self.command_bar.addAction(Action(FIF.IOT, 'Configurar escala'))
        self.information_stack = InformationInterface()
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.command_bar)
        layout.addWidget(CardSeparator())
        layout.addWidget(self.information_stack, Qt.AlignmentFlag.AlignCenter)

        self.setObjectName(text.replace(' ', '-'))

class InformationInterface(OpacityAniStackedWidget):
    """
    Three-way stacked widget to show information about courses
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_no_class_level()
        self.setCurrentIndex(0)


    def create_no_class_level(self) -> None:
        panel = QWidget()
        icon = QLabel()
        icon.setPixmap(QPixmap(Paths.get('no_book')))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle = SubtitleLabel('No classes created')
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout(panel)
        layout.addWidget(icon, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle, Qt.AlignmentFlag.AlignCenter)
        self.addWidget(panel)

    def create_allclasses_level(self) -> None:
        self.classes_area = ScrollArea()
        self.classes_area.setObjectName('all_classes')
        self.classes_area.setWidgetResizable(True)
        self.classes_area.setFrameShape(QFrame.Shape.NoFrame)

    def create_singleclass_level(self) -> None:
        panel = QWidget()
        self.addWidget(panel)
