import datetime
import json
from os.path import exists

from components.course import PUClass
from components.course import search_for_puclasses
from components.database import PUCalendarDatabaseHandler as Db
from components.paths import Paths
from components.schedule import PUCWeek
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QObject

# Temporalmente estoy conectando a la base de datos directamente
# Dentro de poco debe abstraer la funcionalidad de la conexión
# y las queries a una clase específica para, aun más a futuro,
# independizar y comunicar con API a un servidor más elaborado

def get_year_and_value() -> tuple[str]:
    current_month = datetime.datetime.now().month
    current_year = str(datetime.datetime.now().year)

    if current_month >= 12 or current_month <= 6:
        return (current_year, '1')
    else:
        return (current_year, '2')


class MainLogic(QObject):

    # Signals should start with SG identifier

    SGpuclass_search_result: pyqtSignal = pyqtSignal(list)
    SGpuclass_creation_status: pyqtSignal = pyqtSignal(bool, str)
    SGloaded_puclass: pyqtSignal = pyqtSignal(dict)

    def __init__(self) -> None:
        super().__init__()
        
        # Load parameters of application
        with open(Paths.get('parameters'), 'r') as params_file:
            self.parameters = json.load(params_file)
        
        # Prepare app
        self.create_attributes()
        self.init_database_connection()

    

    def init_database_connection(self) -> None:
        # Check if database already exists
        if not self.db.exists(): self.db.create_database()
        else: self.db.connect()

        # retrieve user and create it if non existant
        self.user = self.db.get_user(1) # HARDCODED by now
        if self.user is None: self.user = self.db.create_standard_user()

        # create current user courses
        [self.puclasses.add(PUClass(**puclass)) for puclass in \
            self.db.get_courses(self.user.get('id'))]


    #########################################################
    ###                     Listeners                     ###
    #########################################################

    def app_is_closing(self) -> None:
        """Handles the closing event of the app"""
        pass
    
    def RQsearch_for_puclass(self, search_query: str) -> None:
        """Receives the request to search for a new class"""
        if len(search_query) < 3: return
        self.current_search_result = search_for_puclasses(
            search_query, *get_year_and_value())
        self.send_puclass_search_result()

    def RQcreate_new_puclass(self, index: int, alias: str, color: str) -> None:
        self.create_new_puclass_from_web(
            self.current_search_result[index], alias, color)





    #########################################################
    ###                     Handles                       ###
    #########################################################

    def create_attributes(self) -> None:
        self.week: PUCWeek = PUCWeek(self.parameters.get('block_params'))
        self.db: Db = Db(Paths.get('session_db'))
        self.puclasses: dict = {}
        self.current_search_result: list[dict] | None = None

    def create_new_puclass_from_web(self, web_dict: dict,
                                  alias: str, color: str) -> None:
        if nrc := web_dict.get('nrc') in self.puclasses.keys():
            return self.send_puclass_creation_status(False, 'already')
        self.puclasses[nrc] = (puclass := PUClass(alias, color, **web_dict))
        self.send_puclass_creation_status(True, 'OK')
        self.send_loaded_puclass(puclass.info)




    #########################################################
    ###                     Senders                       ###
    #########################################################

    def send_puclass_search_result(self) -> None:
        self.SGpuclass_search_result.emit(
            ['{} - Sección {} ({})'.format(
                course.get("name"),
                course.get("section"),
                course.get("code")) 
            for course in self.current_search_result])
        
    def send_puclass_creation_status(self, status: bool, reason: str) -> None:
        self.SGpuclass_creation_status.emit(status, reason)

    def send_loaded_puclass(self, puclass: dict) -> None:
        self.SGloaded_puclass.emit(puclass)


    #########################################################
    ###                      Other                        ###
    #########################################################

    def printCourses(self) -> None:
        [print(f'\n{curso}') for curso in self.puclasses]
