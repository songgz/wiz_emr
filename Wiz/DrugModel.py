from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Wiz.BaseModel import *


class DrugModel(QAbstractTableModel):
    def __init__(self):
        super(DrugModel, self).__init__()
        self.list = Drug.select()
        self.names = ['id', 'name', 'pinyin']

    def rowCount(self, index=QModelIndex()):
        return len(self.list)

    def columnCount(self, index=QModelIndex()):
        return 3

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return getattr(self.list[index.row()], self.names[index.column()])


    def setData(self, index, role, value):
        if role == Qt.DisplayRole:
            setattr(self.list[index.row()], self.names[index.column()], value)

