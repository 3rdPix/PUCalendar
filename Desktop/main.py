import sys

from app import PUCalendar

if __name__ == '__main__':

    app = PUCalendar(sys.argv)
    sys.exit(app.exec())
