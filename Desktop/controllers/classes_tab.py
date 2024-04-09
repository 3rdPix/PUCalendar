import datetime

from components import PUClass
from components import search_for_puclasses
from PyQt6.QtCore import pyqtBoundSignal
from PyQt6.QtCore import QObject

def get_year_and_value() -> tuple[str]:
    current_month = datetime.datetime.now().month
    current_year = str(datetime.datetime.now().year)

    if current_month >= 12 or current_month <= 6:
        return (current_year, '1')
    else:
        return (current_year, '2')


class CoursesTabLogic(QObject):

    SG_CourT_search_result: pyqtBoundSignal
    SG_CourT_show_single_puclass_panel: pyqtBoundSignal
    SG_CourT_single_puclass_information: pyqtBoundSignal
    SG_CourT_newpuclass_creation_status: pyqtBoundSignal
    SG_CourT_add_card_to_allpuclass_panel: pyqtBoundSignal

    def __init__(self, puclasses_ref: dict[str, PUClass],
                 parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.puclasses = puclasses_ref

    #########################################################
    ###                     Listeners                     ###
    #########################################################

    def RQsearch_for_puclass(self, search_query: str) -> None:
        """Receives the request to search for a new class"""
        if len(search_query) < 3: return
        self.current_search_result = search_for_puclasses(
            search_query, *get_year_and_value())
        self.send_puclass_search_result()

    def RQcreate_new_puclass(self, index: int, alias: str, color: str) -> None:
        """Receives request to create new class from web information"""
        self.create_new_puclass_from_web(
            self.current_search_result[index], alias, color)
        
    def RQpuclass_clicked(self, _id: str) -> None:
        """Receives request to go to course panel after selecting a course"""

    #########################################################
    ###                     Handles                       ###
    #########################################################

    def send_puclass_search_result(self) -> None:
        self.SG_CourT_search_result.emit(
            ['{} - Sección {} ({})'.format(
                course.get("name"),
                course.get("section"),
                course.get("code")) 
            for course in self.current_search_result])
        
    def create_new_puclass_from_web(self, web_dict: dict,
                                  alias: str, color: str) -> None:
        """Handles the request to create new class from web"""
        if nrc := web_dict.get('nrc') in self.puclasses.keys():
            return self.SG_CourT_newpuclass_creation_status.emit(False, 'already')
        self.puclasses[nrc] = (puclass := PUClass(alias, color, **web_dict))
        self.SG_CourT_newpuclass_creation_status.emit(True, 'OK')
        self.SG_CourT_add_card_to_allpuclass_panel.emit(
            puclass.info.get('alias'), puclass.info.get('color'),
            puclass.info.get('name'), puclass.info.get('code'),
            puclass.info.get('section'))

    def load_single_course_panel(self, _id: str) -> None:
        self.SG_CourT_single_puclass_information.emit(
            self.puclasses.get(_id).info)
        self.SG_CourT_show_single_puclass_panel.emit()
