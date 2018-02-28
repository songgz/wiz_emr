from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Wiz.Conn import *
from Wiz.DrugModel import *


class DrugComboBox(QComboBox):
    def __init__(self, parent=None):
        super(DrugComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        self.filterModel = QSortFilterProxyModel(self)
        self.filterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filterModel.setFilterKeyColumn(-1)

        self.completer = QCompleter(self.filterModel, self)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.completer.setPopup(self.view())
        self.setCompleter(self.completer)

        self.lineEdit().textEdited.connect(self.filter)
        self.completer.activated.connect(self.on_completer_activated)

    def setModel(self, model):
        super(DrugComboBox, self).setModel(model)
        self.filterModel.setSourceModel(model)
        self.completer.setModel(self.filterModel)

    def setModelColumn(self, column):
        self.completer.setCompletionColumn(column)
        super(DrugComboBox, self).setModelColumn(column)

    def view(self):
        return self.completer.popup()

    def index(self):
        return self.currentIndex()

    def filter(self, text):
        self.filterModel.setFilterFixedString(text)

    def on_completer_activated(self, text):
        print(text)
        if text:
            index = self.findText(text)
            self.setCurrentIndex(index)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    combo = DrugComboBox()
    drug = QtSql.QSqlQueryModel()
    drug.setQuery('select name, id, pinyin from drug')
    combo.setModel(DrugModel())
    combo.setModelColumn(1)
    combo.resize(300, 40)
    combo.show()
    sys.exit(app.exec_())