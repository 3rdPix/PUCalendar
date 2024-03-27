from components.course import PUClass
from components.paths import Paths
from components.text import AppText
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QAbstractAnimation
from PyQt6.QtCore import QPropertyAnimation
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QScreen
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QListWidgetItem
from PyQt6.QtWidgets import QStackedWidget
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
from qfluentwidgets import Action
from qfluentwidgets import CaptionLabel
from qfluentwidgets import ColorPickerButton
from qfluentwidgets import CommandBar
from qfluentwidgets import FlowLayout
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import LineEdit
from qfluentwidgets import ListWidget
from qfluentwidgets import MessageBoxBase
from qfluentwidgets import ScrollArea
from qfluentwidgets import setFont
from qfluentwidgets import SubtitleLabel
from qfluentwidgets import TitleLabel
from qfluentwidgets.components.widgets.card_widget import CardSeparator
from qfluentwidgets.components.widgets.card_widget import CardWidget
from qfluentwidgets.components.widgets.card_widget import ElevatedCardWidget


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


class MyPUClassesTab(QFrame):
    """Class that represents the courses tab"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('courses_tab')
        self._init_attr()
        self._init_UI()

    #########################################################
    ###                     Handles                       ###
    #########################################################

    def _init_attr(self) -> None:
        self.vertical_layout: QVBoxLayout = QVBoxLayout(self)
        self.newclass_search_interface = NewClassInterface(self.parent())
        
    def _init_UI(self) -> None:
        # barra de usos
        command_bar = CommandBar(parent=self)
        command_bar.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        command_bar.addActions(self._create_command_bar_actions())
        self.vertical_layout.addWidget(command_bar)

        # separador visual
        self.vertical_layout.addWidget(CardSeparator(self.vertical_layout))

        # panel de cursos
        self.information_panel = InformationPanel(self)
        self.vertical_layout.addWidget(self.information_panel)

        # panel 1
        no_puclass_layer = QWidget(self.information_panel)
        icon = QLabel(no_puclass_layer)
        icon.setPixmap(QPixmap(Paths.get('no_book')))
        # icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle = SubtitleLabel(AppText.NO_CLASS_CREATED, no_puclass_layer)
        # subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout(no_puclass_layer)
        layout.addStretch()
        layout.addWidget(icon)
        layout.addWidget(subtitle)
        layout.addStretch()
        self.information_panel.addWidget(no_puclass_layer)

        # panel 2
        all_puclasses_layer = ScrollArea(self.information_panel)
        all_puclasses_layer.setWidgetResizable(True)
        # all_puclasses_layer.setFrameShape(QFrame.Shape.NoFrame)
        # all_puclasses_layer.setObjectName('scrollarea_layer')
        widget_obejct = QWidget(all_puclasses_layer)
        self.all_puclasses_panel = FlowLayout(widget_obejct)
        all_puclasses_layer.setWidget(widget_obejct)
        self.information_panel.addWidget(all_puclasses_layer)

        # panel 3 ESTOY AQUÍ

    def _create_command_bar_actions(self) -> list[Action]:
        actions = list()

        add_new = Action(FIF.ADD, AppText.CB_ADD_NEW_PUCLASS)
        add_new.triggered.connect(self._CB_add_new_puclass)
        actions.append(add_new)

        delete_puclass = Action(FIF.DELETE, AppText.CB_DELETE_PUCLASS)
        delete_puclass.triggered.connect(self._CB_delete_puclass)
        actions.append(delete_puclass)

        edit_puclass = Action(FIF.EDIT, AppText.CB_EDIT_PUCLASS)
        edit_puclass.triggered.connect(self._CB_edit_puclass)
        actions.append(edit_puclass)

        set_scale = Action(FIF.IOT, AppText.CB_EDIT_SCALE)
        set_scale.triggered.connect(self._CB_edit_scale)
        actions.append(set_scale)

        return actions

    def _CB_add_new_puclass(self) -> None:
        pass

    def _CB_delete_puclass(self) -> None:
        pass

    def _CB_edit_puclass(self) -> None:
        pass

    def _CB_edit_scale(self) -> None:
        pass

    #########################################################
    ###                     Listeners                     ###
    #########################################################

    def add_new(self, course: PUClass) -> None:
        self.loaded_courses[course.info.get('nrc')] = \
            (box := CourseSummaryBox(course))
        self.information_stack.load_course(box)
        self.information_stack.setCurrentIndex(1)

    #########################################################
    ###                     Senders                       ###
    #########################################################

    




class CourseSummaryBox(ElevatedCardWidget):

    def __init__(self, course: PUClass, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)
        self.alias_label = TitleLabel(course.info.get('alias'))
        self.alias_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.alias_label.setStyleSheet(
            f'QLabel{{ font: italic }}'
        )
        self.alias_label.setWordWrap(True)
        self.name_label = SubtitleLabel(course.info.get('name'))
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.name_label.setWordWrap(True)
        self.code_label = SubtitleLabel(course.info.get('code'))
        self.code_label.setAlignment(Qt.AlignmentFlag.AlignCenter)


        color_box = QFrame()
        color_box.setFixedSize(15, 15)
        color_box.setStyleSheet(
            f'QFrame{{ background-color:{course.info.get("color")} }}')
        
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


class InformationPanel(OpacityAniStackedWidget):
    """
    Three-way stacked widget to show information about courses
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.create_no_class_level()
        self.create_allclasses_level()
        self.create_singleclass_level()

    def create_no_class_level(self) -> None:
        self.noclass_panel = QWidget(self)
        icon = QLabel()
        icon.setPixmap(QPixmap(Paths.get('no_book')))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle = SubtitleLabel('No classes created')
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout(self.noclass_panel)
        layout.addStretch()
        layout.addWidget(icon)
        layout.addWidget(subtitle)
        layout.addStretch()
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

    def load_course(self, box: CourseSummaryBox) -> None:
        self.widget_flow.addWidget(box)
        print(box.alias_label.text())

class NewClassInterface(MessageBoxBase):

    do_search = pyqtSignal(str)
    newclass_fromWeb = pyqtSignal(int, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_UI()
        self.search_line.returnPressed.connect(self.search_for)
        self.accepted.connect(self.send_selection)

    def init_UI(self) -> None:
        search_label = CaptionLabel('Buscar curso:')
        
        self.search_line = LineEdit()
        self.search_line.setClearButtonEnabled(True)
        self.search_line.setPlaceholderText('Ingresar nombre o sigla')
        self.list_view = ListWidget()
        alias_label = CaptionLabel('Alias:')
        self.alias_line = LineEdit()
        self.alias_line.setClearButtonEnabled(True)
        self.alias_line.setPlaceholderText('Cómo te refieres a este ramo')
        self.alias_line.setEnabled(False)
        self.alias_line.setMaxLength(10)
        color_label = CaptionLabel('Color:')
        self.color_box = ColorPickerButton(QColor("#5012aaa2"), 'color_btn')
        self.color_box.setFixedSize(20, 20)
        self.color_box.setEnabled(False)
        self.list_view.itemClicked.connect(
            lambda: [self.yesButton.setEnabled(True),
                     self.alias_line.setEnabled(True),
                     self.color_box.setEnabled(True)])
        lay = QHBoxLayout()
        lay.addWidget(search_label)
        lay.addWidget(self.search_line)
        lay2 = QHBoxLayout()
        lay2.addWidget(alias_label)
        lay2.addWidget(self.alias_line)
        lay2.addWidget(color_label)
        lay2.addWidget(self.color_box)
        self.viewLayout.addLayout(lay)
        self.viewLayout.addWidget(self.list_view)
        self.viewLayout.addLayout(lay2)
        self.yesButton.setDisabled(True)
        self.yesButton.setText('Confirmar')
        self.cancelButton.setText('Cancelar')

    def send_selection(self) -> None:
        self.newclass_fromWeb.emit(
            self.list_view.currentRow(),
            self.alias_line.text(),
            self.color_box.color.name()
        )
        self.clearinterface()

    def search_for(self) -> None:
        self.list_view.setCurrentRow(-1)
        self.yesButton.setEnabled(False)
        self.do_search.emit(self.search_line.text())
        
        

    def show_search_result(self, result_list: list[str]) -> None:
        self.list_view.clear()
        self.list_view.addItems(result_list)

    def clearinterface(self) -> None:
        self.list_view.clear()
        self.search_line.clear()
        self.alias_line.clear()
        self.alias_line.setEnabled(False)
        self.color_box.setEnabled(False)
        self.yesButton.setEnabled(False)
