from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QGridLayout
from PyQt6.QtGui import QPaintEvent, QPixmap, QPainter, QLinearGradient, QColor, QBrush, QPainterPath, QResizeEvent
from PyQt6.QtCore import Qt, QRectF
from qfluentwidgets import isDarkTheme, ScrollArea, FlowLayout, SubtitleLabel, SmoothScrollArea
from components.summary_box import InfoBox

class TimersInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_UI()

    def _create_UI(self) -> None:
        
        # scroll adjustments
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)

        # 