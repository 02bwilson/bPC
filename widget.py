from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout

from cpu import bPC_cpu
from gpu import bPC_gpu


class bPC_Widget(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = None
        self.cpu_widget = None


        self.layout = QGridLayout()


        self.cpu_widget = bPC_cpu()
        self.gpu_widget = bPC_gpu()

        self.layout.addWidget(self.cpu_widget, 0, 0, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.gpu_widget, 1, 0, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)


        self.setLayout(self.layout)
