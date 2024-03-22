from PyQt6.QtCore import QObject, pyqtSignal
from os.path import exists
from components.paths import Paths
from components.schedule import PUCWeek
from components.course import Course, search_for_courses
from components.database import PUCalendarDatabaseHandler as Db
import json

# Temporalmente estoy conectando a la base de datos directamente
# Dentro de poco debe abstraer la funcionalidad de la conexión
# y las queries a una clase específica para, aun más a futuro,
# independizar y comunicar con API a un servidor más elaborado



class MainLogic(QObject):

    search_result: pyqtSignal = pyqtSignal(list)

    def __init__(self) -> None:
        super().__init__()
        with open(Paths.get('parameters'), 'r') as params_file:
            self.parameters = json.load(params_file)
        self.week = PUCWeek(self.parameters.get('block_params'))
        self.db = Db(Paths.get('session_db'))

    def initSession(self) -> None:
        # Check if database already exists
        if not self.db.exists(): self.db.create_database()
        else: self.db.connect()

        # retrieve user and create it if non existant
        self.user = self.db.get_user(1) # HARDCODED by now
        if self.user is None: self.user = self.db.create_standard_user()

        # create current user courses
        self.courses = list()
        for course in self.db.get_courses(self.user.get('id')):
            self.courses.append(Course(**course))
        self.db.disconnect()

    def printCourses(self) -> None:
        [print(f'\n{curso}') for curso in self.courses]

    def newclass_search(self, text: str) -> None:
        if len(text) < 3: return
        available = search_for_courses(text, '2024', '1')
        shown_list = list()
        for course in available:
            shown_list.append(
                f'{course.get("name")} - Sección {course.get("section")} ({course.get("code")})'
            )
        self.search_result.emit(shown_list)

