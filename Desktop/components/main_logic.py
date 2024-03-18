from PyQt6.QtCore import QObject
from os.path import exists
from components.paths import Paths
from components.schedule import PUCWeek
from components.course import Course
import sqlite3
import json

# Temporalmente estoy conectando a la base de datos directamente
# Dentro de poco debe abstraer la funcionalidad de la conexión
# y las queries a una clase específica para, aun más a futuro,
# independizar y comunicar con API a un servidor más elaborado

def dict_factory(cursor, row) -> dict:
    dictionary = {}
    for idx, col in enumerate(cursor.description):
        dictionary[col[0]] = row[idx]
    return dictionary

class MainLogic(QObject):

    def __init__(self) -> None:
        super().__init__()
        with open(Paths.get('parameters'), 'r') as params_file:
            self.parameters = json.load(params_file)
        self.week = PUCWeek(self.parameters.get('block_params'))

    def initSession(self) -> None:
        # Check if database already exists
        if not exists(Paths.get('session_db')): self.create_db()
        else: self.db_connection = sqlite3.connect(Paths.get('session_db'))
        self.db_connection.row_factory = dict_factory
        self.db_cursor = self.db_connection.cursor()

        # retrieve user and create it if non existant
        self.db_cursor.execute("SELECT * FROM Users WHERE id = 1")
        self.usuario = self.db_cursor.fetchone()
        if self.usuario is None:
            self.usuario = {"id": 1, "name": 'PUCsuario', "mail": 'example@example.com'}
            self.db_cursor.execute(
                "INSERT INTO Users (id, name, email) VALUES (?, ?, ?)",
                (self.usuario['id'], self.usuario['name'], self.usuario['mail']))
            self.db_connection.commit()

        # retrieve courses
        self.db_cursor.execute(f"""
            SELECT Courses.*, Users_Courses.alias, Users_Courses.color, Users_Courses.dedicated_minutes
            FROM Users_Courses
            JOIN Courses ON Users_Courses.course_id = Courses.id
            WHERE Users_Courses.user_id = {self.usuario.get('id')}""")

        # create current user courses
        self.courses = list()
        found_courses: list[dict] = self.db_cursor.fetchall()
        for course in found_courses:
            self.courses.append(Course(**course))
        self.db_connection.close()

    def printCourses(self) -> None:
        [print(f'\n{curso}') for curso in self.courses]


    def create_db(self) -> None:
        print('CREATING DATABASE')
        self.db_connection = sqlite3.connect(Paths.get('session_db'))
        
        # Create users table
        self.db_connection.execute("""
            CREATE TABLE Users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT    
            )""")
        
        # Create courses table
        self.db_connection.execute("""
            CREATE TABLE Courses (
                id INTEGER PRIMARY KEY,
                name TEXT,
                nrc TEXT,
                code INTEGER,
                professor TEXT,
                campus TEXT,
                section INTEGER,
                dates TEXT
            )""")
        
        # Create users_courses table
        self.db_connection.execute("""
            CREATE TABLE Users_Courses (
                user_id INTEGER,
                course_id INTEGER,
                dedicated_minutes INTEGER,
                alias TEXT,
                color TEXT,
                FOREIGN KEY(user_id) REFERENCES Users(id),
                FOREIGN KEY(course_id) REFERENCES Courses(id)
            )""")
        
        self.db_connection.commit()

