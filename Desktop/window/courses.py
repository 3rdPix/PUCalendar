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

    SGsearch_for_puclass: pyqtSignal = pyqtSignal(str)
    SGselect_newclass: pyqtSignal = pyqtSignal(int, str, str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('courses_tab')
        self._init_attr()
        self._init_UI()
        self._connect_SG()

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
        self.vertical_layout.addWidget(CardSeparator())

        # panel de cursos
        self.information_panel = OpacityAniStackedWidget(self)
        self.vertical_layout.addWidget(self.information_panel)

        # panel 1
        no_puclass_layer = QWidget(self.information_panel)
        icon = QLabel(no_puclass_layer)
        icon.setPixmap(QPixmap(Paths.get('no_book')))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle = SubtitleLabel(AppText.NO_CLASS_CREATED, no_puclass_layer)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        # placeholder widget
        placeholder_widget = QWidget(self)
        self.information_panel.addWidget(placeholder_widget)

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
        self.newclass_search_interface.show()

    def _CB_delete_puclass(self) -> None:
        pass

    def _CB_edit_puclass(self) -> None:
        pass

    def _CB_edit_scale(self) -> None:
        pass

    def _connect_SG(self) -> None:
        self.newclass_search_interface.SGsearch_for_puclass.connect(
            self.search_for_puclass)
        
        self.newclass_search_interface.SGselect_puclass.connect(
            self.send_newclass_selection)

    #########################################################
    ###                     Listeners                     ###
    #########################################################

    def add_new(self, puclass: dict) -> None:
        infobox = PUClassInfoBox(**puclass)
        self.all_puclasses_panel.addWidget(infobox)
        self.information_panel.setCurrentIndex(1)

    def show_search_results(self, results: list[dict]) -> None:
        self.newclass_search_interface.show_search_result(results)

    #########################################################
    ###                     Senders                       ###
    #########################################################

    def search_for_puclass(self, search_query: str) -> None:
        self.SGsearch_for_puclass.emit(search_query)

    def send_newclass_selection(self, index: int,
                                alias: str, color: str) -> None:
        self.SGselect_newclass.emit(index, alias, color)


class PUClassInfoBox(ElevatedCardWidget):
    """Flotant box to be shown in all_puclasses_panel"""

    def __init__(self, alias: str, color: str,
                 name: str, code: str, section: int, parent=None, **kwargs):
        super().__init__(parent)
        # self.setFixedSize(200, 200)
        layout = QVBoxLayout(self)
        
        sub_layout_1 = QHBoxLayout()
        color_box = ColorPickerButton(QColor(color), '', parent=self)
        alias_label = TitleLabel(text=alias, parent=self)
        sub_layout_1.addWidget(color_box, Qt.AlignmentFlag.AlignCenter)
        sub_layout_1.addWidget(alias_label, Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(sub_layout_1)

        layout.addWidget(CardSeparator())

        description =   CaptionLabel(
            text=f'({code}-{section} {name})', parent=self)
        layout.addWidget(description)

class NewClassInterface(MessageBoxBase):

    SGsearch_for_puclass = pyqtSignal(str)
    SGselect_puclass = pyqtSignal(int, str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.hide()
        self._init_UI() # creates interface elements
        self._connect_signals() # connect signals

    #########################################################
    ###                     Handles                       ###
    #########################################################

    def _init_UI(self) -> None:
        # Search block
        sub_layout1 = QHBoxLayout()
        search_label = CaptionLabel(text=AppText.NC_SEARCH)
        self.search_linedit = LineEdit(self)
        self.search_linedit.setClearButtonEnabled(True)
        self.search_linedit.setPlaceholderText(AppText.NC_SEARCH_PLACEHOLDER)
        sub_layout1.addWidget(search_label)
        sub_layout1.addWidget(self.search_linedit)
        self.viewLayout.addLayout(sub_layout1)

        # Results block
        self.search_result_view = ListWidget(self)
        self.viewLayout.addWidget(self.search_result_view)

        # Other parameters
        sub_layout2 = QHBoxLayout()
        alias_label = CaptionLabel(text=AppText.NC_ALIAS)
        self.alias_linedit = LineEdit(self)
        self.alias_linedit.setClearButtonEnabled(True)
        self.alias_linedit.setPlaceholderText(AppText.NC_ALIAS_PLACEHOLDER)
        self.alias_linedit.setEnabled(False)
        self.alias_linedit.setMaxLength(10)
        color_label = CaptionLabel(AppText.NC_COLOR)
        self.color_selector = ColorPickerButton(
            QColor('#5010aaa2'), AppText.NC_COLOR_TITLE)
        self.color_selector.setEnabled(False)
        sub_layout2.addWidget(alias_label)
        sub_layout2.addWidget(self.alias_linedit)
        sub_layout2.addWidget(color_label)
        sub_layout2.addWidget(self.color_selector)
        self.viewLayout.addLayout(sub_layout2)

        # final text
        self.yesButton.setText(AppText.NC_CONFIRM)
        self.yesButton.setEnabled(False)
        self.cancelButton.setText(AppText.NC_CANCEL)

    def _connect_signals(self) -> None:
        self.search_linedit.returnPressed.connect(
            self.search_for_puclass)
        
        self.search_result_view.itemClicked.connect(
            self._enable_buttons)
        
        self.alias_linedit.textChanged.connect(
            self._check_selection_completed)

        self.accepted.connect(
            self.send_selection)

    def _enable_buttons(self) -> None:
        self.alias_linedit.setEnabled(True)
        self.color_selector.setEnabled(True)

    def _clearinterface(self) -> None:
        self.search_result_view.clear()
        self.search_linedit.clear()
        self.alias_linedit.clear()
        self.alias_linedit.setEnabled(False)
        self.color_selector.setEnabled(False)
        self.yesButton.setEnabled(False)

    def _check_selection_completed(self) -> None:
        if self.search_result_view.currentRow() == -1: return
        if self.alias_linedit.text() == '':
            self.yesButton.setEnabled(False)
            return
        self.yesButton.setEnabled(True)

    #########################################################
    ###                     Senders                       ###
    #########################################################

    def send_selection(self) -> None:
        self.SGselect_puclass.emit(
            self.search_result_view.currentRow(),
            self.alias_linedit.text(),
            self.color_selector.color.name())
        self._clearinterface()

    def search_for_puclass(self) -> None:
        self.search_result_view.setCurrentRow(-1)
        self.SGsearch_for_puclass.emit(self.search_linedit.text())
    
    #########################################################
    ###                     Listeners                     ###
    #########################################################
        
    def show_search_result(self, result_list: list[str]) -> None:
        self.search_result_view.clear()
        self.search_result_view.addItems(result_list)    