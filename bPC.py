import sys

from PyQt6.QtWidgets import QApplication
from mainwindow import bPC_MW

if __name__ == "__main__":
    app = QApplication([])
    window = bPC_MW()
    window.show()
    sys.exit(app.exec())