import threading

from base import entryBase
from data_fetcher import bPC_DF


class bPC_cpu(entryBase):

    def __init__(self):
        super().__init__('CPU')
        self.data = None
        setup_thrd = threading.Thread(target=self.setup)
        setup_thrd.start()

    def setup(self):
        self.data = self.get_data()





