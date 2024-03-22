from PyQt6.QtWidgets import QGraphicsOpacityEffect, QFrame, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QStackedWidget
from PyQt6.QtCore import Qt, QPropertyAnimation, QAbstractAnimation
from PyQt6.QtGui import QKeyEvent, QPixmap
from qfluentwidgets import  FlowLayout, TitleLabel, ScrollArea, SubtitleLabel, setFont, CommandBar, Action, FluentIcon as FIF
from qfluentwidgets.components.widgets.card_widget import CardWidget, CardSeparator, ElevatedCardWidget
from components.paths import Paths
from components.course import Course

class OpacityAniStackedWidget(QStackedWidget):
    """ Stacked widget with fade in and fade out animation """

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.__create_animations()

    def setCurrentIndex(self, index: int) -> None:
        if index == self.currentIndex(): return
        if not self.widget(index): return # avoids going to nonexisting index
        
        # Current index hides, target index shows
        self.currentWidget().setGraphicsEffect(self._opacity1)
        self.widget(index).setGraphicsEffect(self._opacity2)

        # Show target index (currently invisible)
        self.widget(index).show()

        # Start animations
        self._opacityUp.finished.connect(
            lambda: self.rst_effects(self.currentWidget(), self.widget(index)))
        self._opacityDown.start(QAbstractAnimation.DeletionPolicy.KeepWhenStopped)
        self._opacityUp.start(QAbstractAnimation.DeletionPolicy.KeepWhenStopped)

    def rst_effects(self, w_hidden: QWidget, w_shown: QWidget) -> None:
        super().setCurrentWidget(w_shown)
        w_hidden.setGraphicsEffect(None)
        w_shown.setGraphicsEffect(None)
        self.__create_animations()

    def __create_animations(self) -> None:

        self._opacity1 = QGraphicsOpacityEffect(self)
        self._opacity2 = QGraphicsOpacityEffect(self)
        self._opacity2.setOpacity(0.0)

        ## Animation for both opacities
        self._opacityDown = QPropertyAnimation(self._opacity1, b'opacity')
        self._opacityDown.setStartValue(1.0)
        self._opacityDown.setEndValue(0.0)

        self._opacityUp = QPropertyAnimation(self._opacity2, b'opacity')
        self._opacityUp.setStartValue(0.0)
        self._opacityUp.setEndValue(1.0)

    def setDuration(self, ms: int) -> None:
        """Sets the duration of the transition between widgets"""
        self._opacityUp.setDuration(ms)
        self._opacityDown.setDuration(ms)

    def setCurrentWidget(self, w: QWidget) -> None:
        self.setCurrentIndex(self.indexOf(w))

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

    def keyPressEvent(self, a0: QKeyEvent | None) -> None:
        print(a0.text())
        self.information_stack.setCurrentIndex(int(a0.text()))
        return super().keyPressEvent(a0)

class InformationInterface(OpacityAniStackedWidget):
    """
    Three-way stacked widget to show information about courses
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_no_class_level()
        self.create_allclasses_level()
        self.create_singleclass_level()
        self.load_course(Course('hard', 'orange', name='Mecánica de Fluidos', code='ICH1104'))

    def create_no_class_level(self) -> None:
        self.noclass_panel = QWidget(self)
        icon = QLabel()
        icon.setPixmap(QPixmap(Paths.get('no_book')))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle = SubtitleLabel('No classes created')
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout(self.noclass_panel)
        layout.addWidget(icon, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle, Qt.AlignmentFlag.AlignCenter)
        self.addWidget(self.noclass_panel)

    def create_allclasses_level(self) -> None:
        self.allclass_panel = ScrollArea(self)
        self.allclass_panel.setObjectName('all_classes')
        self.allclass_panel.setWidgetResizable(True)
        self.allclass_panel.setFrameShape(QFrame.Shape.NoFrame)

        self.widget_object = QWidget()
        self.widget_flow = FlowLayout(self.widget_object)
        self.allclass_panel.setWidget(self.widget_object)
        self.addWidget(self.allclass_panel)

    def create_singleclass_level(self) -> None:
        self.singleclass_panel = QWidget(self)
        self.addWidget(self.singleclass_panel)

    def load_course(self, course: Course) -> None:
        self.widget_flow.addWidget(
            CourseSummaryBox(course))


class CourseSummaryBox(CardWidget):

    def __init__(self, course: Course, parent=None):
        super().__init__(parent)
        self.alias_label = TitleLabel(course.this_class.get('alias'))
        self.alias_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.alias_label.setStyleSheet(
            f'QLabel{{ font: italic }}'
        )
        self.name_label = SubtitleLabel(course.this_class.get('name'))
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setStyleSheet(
            f'QLabel {{ font: 8pt }}'
        )
        self.code_label = SubtitleLabel(course.this_class.get('code'))
        self.code_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.code_label.setStyleSheet(
            f'QLabel {{ font: 9pt }}'
        )

        color_box = QFrame()
        color_box.setFixedSize(15, 15)
        color_box.setStyleSheet(
            f'QFrame{{ background-color:{course.this_class.get("color")} }}')
        
        distribution = QVBoxLayout(self)
        lateral_1 = QHBoxLayout()
        lateral_1.addStretch()
        lateral_1.addWidget(color_box)
        lateral_1.addWidget(self.alias_label)
        lateral_1.addStretch()
        distribution.addLayout(lateral_1)
        distribution.addWidget(self.name_label)
        distribution.addWidget(self.code_label)
        distribution.addWidget(CardSeparator())
