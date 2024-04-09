import datetime
import json

from components import SGMainLogic
from components.course import PUClass
from components.database import PUCalendarDatabaseHandler as Db
from components.paths import Paths
from components.schedule import PUCWeek
from controllers import CoursesTabLogic

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


class MainLogic(SGMainLogic):

    def __init__(self) -> None:
        super().__init__()
        
        # Load parameters of application
        with open(Paths.get('parameters'), 'r') as params_file:
            self.parameters = json.load(params_file)
        
        # Prepare app
        self._create_attributes()
        self._init_database_connection()
        self.__init__sg()

    #########################################################
    ###                     Listeners                     ###
    #########################################################
    
    def RQsearch_for_puclass(self, search_query: str) -> None:
        self.CourT.RQsearch_for_puclass(search_query)

    def RQcreate_new_puclass(self, index: int, alias: str, color: str) -> None:
        self.CourT.RQcreate_new_puclass(index, alias, color)

    def RQpuclass_clicked(self, _id: str) -> None:
        self.CourT.RQpuclass_clicked(_id)

    #########################################################
    ###                     Handles                       ###
    #########################################################

    def _create_attributes(self) -> None:
        self.week: PUCWeek = PUCWeek(self.parameters.get('block_params'))
        self.db: Db = Db(Paths.get('session_db'))
        self.puclasses: dict[str, PUClass] = {}
        self.current_search_result: list[dict] | None = None
        self.CourT = CoursesTabLogic(self.puclasses, parent=self)

    def _init_database_connection(self) -> None:
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
    ###                     Senders                       ###
    #########################################################


    #########################################################
    ###                  SG Shenanigans                   ###
    #########################################################

    def __init__sg(self) -> None:
        """Self's bound signals"""
        
        self.CourT.SG_CourT_search_result = self.SG_CourT_search_result
        self.CourT.SG_CourT_show_single_puclass_panel = self.SG_CourT_show_single_puclass_panel
        self.CourT.SG_CourT_single_puclass_information = self.SG_CourT_single_puclass_information
        self.CourT.SG_CourT_newpuclass_creation_status = self.SG_CourT_newpuclass_creation_status
        self.CourT.SG_CourT_add_card_to_allpuclass_panel = self.SG_CourT_add_card_to_allpuclass_panel
