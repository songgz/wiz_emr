from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Wiz.Conn import *





if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    combo = QComboBox()
    combo.setEditable(True)
    drug = QtSql.QSqlQueryModel()
    drug.setQuery('select name, id, pinyin from drug')
    filterModel = QSortFilterProxyModel()
    filterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
    filterModel.setFilterKeyColumn(1)
    filterModel.setSourceModel(drug)
    combo.setModel(filterModel)
    #completer = QCompleter()
    #combo.setCompleter(completer)
    #combo.completer().setCompletionMode(QCompleter.PopupCompletion)
    def filter(text):
        print(text)
        combo.model().setFilterFixedString(text)

    combo.lineEdit().textEdited.connect(filter)
    combo.resize(300, 40)
    combo.show()
    sys.exit(app.exec_())