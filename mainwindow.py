import sys

from PyQt6.QtWidgets import QMainWindow
import qdarktheme

from widget import bPC_Widget


class bPC_MW(QMainWindow):
    _VERSION_ = "1.0"

    def __init__(self):
        super().__init__()

        qdarktheme.setup_theme('dark')
        self.setWindowTitle("bPC v{}".format(self._VERSION_))
        self.setFixedSize(600, 500)

        self.widget = bPC_Widget()

        self.setCentralWidget(self.widget)

    def closeEvent(self):
        sys.exit()
