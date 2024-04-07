from PyQt6.QtCore import QObject, pyqtSignal


class SGMainLogic(QObject):
    """Class that contains signals of the main logic"""

    # Courses Tab signals    
    SG_CourT_search_result: pyqtSignal = pyqtSignal(list)
    SG_CourT_show_single_puclass_panel: pyqtSignal = pyqtSignal()
    SG_CourT_single_puclass_information: pyqtSignal = pyqtSignal(dict)
    SG_CourT_newpuclass_creation_status: pyqtSignal = pyqtSignal(bool, str)
    SG_CourT_add_card_to_allpuclass_panel: pyqtSignal = pyqtSignal(str, str, str, str, int)
