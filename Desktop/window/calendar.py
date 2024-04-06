from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QVBoxLayout
from qfluentwidgets import setFont
from qfluentwidgets import SubtitleLabel
from qfluentwidgets import DisplayLabel
from qfluentwidgets import FlipView
from qfluentwidgets import CaptionLabel
from qfluentwidgets import CommandBar
from qfluentwidgets import LineEdit
from qfluentwidgets.components.widgets.card_widget import CardSeparator
from typing import Protocol
from components.text import AppText


class CalendarTab(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self._init_attr()
        self._init_UI()

    def _init_attr(self) -> None:
        self._cells: list[QFrame] = list()
        self.setObjectName('calendar_tab')

    def _init_UI(self) -> None:
        tab_layout = QVBoxLayout(self)
        
        self._date_command_bar = CommandBar()

        self._current_month_label = SubtitleLabel('_current_month_label')
        self._date_command_bar.addWidget(self._current_month_label)
        self._date_command_bar.addWidget(CardSeparator())
        self._search_box = LineEdit()
        self._search_box.setPlaceholderText(AppText.CALBAR_SEARCH_LINE)
        tab_layout.addWidget(self._date_command_bar)
        tab_layout.addWidget(CardSeparator())

        self._calendar = Calendar()
        tab_layout.addWidget(self._calendar,
                             Qt.AlignmentFlag.AlignBottom)

class DateCell(Protocol):

    date: DisplayLabel

class Calendar(QWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._create_attr()
        self._init_UI()
        

    def _create_attr(self) -> None:
        self._cells: list[QFrame] = list()

    def _init_UI(self) -> None:
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        for row_index in range(6):
            for column_index in range(7):
                layout.addWidget(
                    new := self._create_cell(),
                    row_index, column_index)
                self._cells.append(new)
        
    def _create_cell(cls) -> QFrame:

        def setDay(cls: DateCell, to: str) -> None:
            cls.date.setText(to)

        give = QFrame(cls)
        give.setMinimumSize(30, 30)
        give.setFrameShape(QFrame.Shape.Box)

        date_number_label = QLabel('0', give)
        setattr(give, 'date', date_number_label)
        setattr(give, 'setDate', setDay)
        return give