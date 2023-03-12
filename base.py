import threading

import psutil
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap, QMovie, QStandardItemModel, QStandardItem
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QTableView, QHeaderView

from data_fetcher import bPC_DF


class entryBase(QWidget):
    _SKIP_TABLE = ["python_version", "hz_actual", "hz_advertised", "cpuinfo_version", "cpuinfo_version_string"]
    _RENAME_TABLE = {'count': 'Cores'}
    def __init__(self, hw):
        super().__init__()

        self.hw = hw
        # Setup vars
        self.layout = None
        self.img_pixmap = None
        self.img = None
        self.label = None
        self.clk_temp_label = None
        self.name = None
        self.entries = None
        self.table = None
        self.table_model = None
        self.data_fetcher = None
        self.ft = None

        self.ft = True

        self.data_fetcher = bPC_DF()

        # Set size to about half the screen
        self.setFixedSize(550, 225)

        # Set border around widget
        self.setStyleSheet("border: 2px solid Gray;")

        # Setup layout
        self.layout = QGridLayout()

        # Setup loading icon
        self.img_movie = QMovie('images/loading.gif')
        self.img_movie.setScaledSize(QSize(90, 90))
        self.img_movie.start()
        self.img = QLabel()
        self.img.setMovie(self.img_movie)
        self.table = QTableView()
        self.table.setFixedWidth(375)
        self.table_model = QStandardItemModel()
        self.table_model.setHorizontalHeaderLabels(['ITEM', 'VALUE'])
        self.table.verticalHeader().setVisible(False)
        self.table.setModel(self.table_model)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)

        # CPU Title Label setup
        self.label = QLabel("Getting {} info".format(self.hw))
        self.label.setFixedSize(150, 30)

        # CPU Speed/Temp setup
        self.clk_temp_label = QLabel("")
        self.clk_temp_label.setFixedSize(150, 30)

        align = Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter
        self.layout.addWidget(self.img, 0, 0, 2, 2, alignment=align)
        self.layout.addWidget(self.table, 0, 2, 4, 2, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout.addWidget(self.label, 2, 0, 1, 2, alignment=align)
        self.layout.addWidget(self.clk_temp_label, 3, 0, 1, 2, alignment=align)

        self.setLayout(self.layout)


    def get_data(self):
        hw = self.hw
        self.data_fetcher.get_data(hw)
        threading.Timer(2.25, self.update_data).start()

    def update_data(self):
        threading.Timer(5, self.update_data).start()
        if self.data_fetcher.data not in[[], None]:
                if self.hw == "CPU":
                    # Add CPU FREQ Data
                    self.data_fetcher.get_cpu_freq()
                    self.clk_temp_label.setText(str(self.data_fetcher.data.get('current_freq')))
                    self.clk_temp_label.setText(str("{:.2f}".format(round(self.data_fetcher.data.get('current_freq'), 2))) + "GHz")
                    self.clk_temp_label.setToolTip(str(self.data_fetcher.data.get('current_freq')) + ' GHz')



                    if self.ft:

                        self.ft = False
                        self.data_fetcher.data.move_to_end('count', last=False)
                        for item in self._RENAME_TABLE:
                            self.data_fetcher.data[self._RENAME_TABLE.get(item)] = self.data_fetcher.data[item]
                            del self.data_fetcher.data[item]
                        cpu = self.data_fetcher.data.get('brand_raw', 'Getting CPU info...')
                        brand = self.data_fetcher.data.get('vendor_id_raw', 'N/A')
                        self.label.setText(cpu)

                        # Setup nice ordering
                        self.data_fetcher.data.move_to_end('Cores', last=False)
                        self.data_fetcher.data.move_to_end('current_freq', last=False)

                        if 'amd' in brand.lower():
                            self.img.setPixmap(QPixmap("images/amd.png").scaledToWidth(90))
                        elif 'intel' in brand.lower():
                            self.img.setPixmap(QPixmap("images/intel.png").scaledToWidth(90))
                        else:
                            self.img.setPixmap(QPixmap("images/cpu.png").scaledToWidth(90))
                        for entry in self.data_fetcher.data.keys():
                            if entry not in self._SKIP_TABLE:
                                self.table_model.appendRow([QStandardItem(entry), QStandardItem(str(self.data_fetcher.data.get(entry)))])
                                self.table.resizeRowsToContents()
                    cnt = 0
                    for entry in self.data_fetcher.data.keys():
                        if entry not in self._SKIP_TABLE:
                            self.table_model.setItem(cnt, 1, QStandardItem(str(self.data_fetcher.data.get(entry))))
                            cnt += 1
                            self.table.resizeRowsToContents()


