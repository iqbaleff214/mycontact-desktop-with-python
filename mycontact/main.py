
import sys

from PyQt5.QtWidgets import QApplication

from .database import create_connection
from .views import Window

def main():
    app = QApplication(sys.argv)

    if not create_connection("mycontact.sqlite"):
        sys.exit(1)

    win = Window()
    win.show()

    sys.exit(app.exec())