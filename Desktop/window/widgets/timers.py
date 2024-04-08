from components.summary_box import InfoBox
from PyQt6.QtCore import QRectF
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush
from PyQt6.QtGui import QColor
from PyQt6.QtGui import QLinearGradient
from PyQt6.QtGui import QPainter
from PyQt6.QtGui import QPainterPath
from PyQt6.QtGui import QPaintEvent
from PyQt6.QtGui import QPixmap
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
from qfluentwidgets import FlowLayout
from qfluentwidgets import isDarkTheme
from qfluentwidgets import ScrollArea
from qfluentwidgets import SmoothScrollArea
from qfluentwidgets import SubtitleLabel

class TimersInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._create_UI()

    def _create_UI(self) -> None:
        
        # scroll adjustments
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)

        #
