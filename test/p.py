class Model(QtCore.QAbstractTableModel):
    def __init__(self):
        super(Model, self).__init__()
        self.table = [[row, choices[0]] for row in rows]
    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.table)
    def columnCount(self, index=QtCore.QModelIndex()):
        return 2
    def flags(self, index):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            return self.table[index.row()][index.column()]
    def setData(self, index, role, value):
        if role == QtCore.Qt.DisplayRole:
            self.table[index.row()][index.column()] = value
