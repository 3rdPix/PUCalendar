from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QGridLayout
from qfluentwidgets import setFont
from qfluentwidgets import SubtitleLabel
from qfluentwidgets import DisplayLabel
from typing import Protocol


class CalendarTab(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignmentFlag.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))

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

        def setDate(cls: DateCell, to: str) -> None:
            cls.date.setText(to)

        give = QFrame(cls, Qt.WindowType.FramelessWindowHint)
        date_number_label = DisplayLabel(give)
        setattr(give, 'date', date_number_label)
        setattr(give, 'setDate', setDate)
        return give