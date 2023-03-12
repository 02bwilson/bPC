from base import entryBase


class bPC_gpu(entryBase):

    def __init__(self):
        super().__init__('GPU')

        self.data = None
        self.setup()

    def setup(self):
        self.data = self.get_data()

