import sqlite3
from os.path import exists

def dict_factory(cursor, row) -> dict:
    dictionary = {}
    for idx, col in enumerate(cursor.description):
        dictionary[col[0]] = row[idx]
    return dictionary

class PUCalendarDatabaseHandler:
    """
    Transitory class to work on the app while connecting to local database
    to simulate later connection to online database
    """
    def __init__(self, dir: str) -> None:
        self.dir = dir

    def exists(self) -> bool:
        return exists(self.dir)
    
    def create_database(self) -> None:
        self.db_connection = sqlite3.connect(self.dir)
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
                dedicated_time INTEGER,
                alias TEXT,
                color TEXT,
                FOREIGN KEY(user_id) REFERENCES Users(id),
                FOREIGN KEY(course_id) REFERENCES Courses(id)
            )""")
        
        self.db_connection.commit()
        self.db_connection.row_factory = dict_factory
        self.db_cursor = self.db_connection.cursor()

    def connect(self) -> None:
        self.db_connection = sqlite3.connect(self.dir)
        self.db_connection.row_factory = dict_factory
        self.db_cursor = self.db_connection.cursor()

    def get_user(self, id: int) -> dict[str, int|str]|None:
        self.db_cursor.execute(f"SELECT * FROM Users WHERE id = ?", (id, ))
        return self.db_cursor.fetchone()
        
    def create_standard_user(self) -> dict[str, int|str]:
        user = {"id": 1, "name": 'PUCsuario', "mail": 'example@example.com'}
        self.db_cursor.execute(
                "INSERT INTO Users (id, name, email) VALUES (?, ?, ?)",
                (user['id'], user['name'], user['mail']))
        self.db_connection.commit()
        return user
    
    def get_courses(self, user_id: int) -> list[dict]|None:
        self.db_cursor.execute(f"""
            SELECT Courses.*, Users_Courses.alias, Users_Courses.color, Users_Courses.dedicated_time
            FROM Users_Courses
            JOIN Courses ON Users_Courses.course_id = Courses.id
            WHERE Users_Courses.user_id = ?""", (user_id, ))
        return self.db_cursor.fetchall()
    
    def disconnect(self) -> None:
        self.db_connection.close()