from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class AutoComboBox(QComboBox):
    def __init__(self, parent=None):
        super(AutoComboBox, self).__init__(parent)

        self.setFocusPolicy(Qt.StrongFocus)
        self.setEditable(True)

        self.filterModel = QSortFilterProxyModel(self)
        self.filterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.filterModel.setSourceModel(self.model())
        self.filterModel.setFilterKeyColumn(2);

        self.completer = QCompleter(self.filterModel, self)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.completer.setCompletionColumn(0)
        self.setCompleter(self.completer)

        self.lineEdit().textEdited.connect(self.filter)
        self.completer.activated.connect(self.on_completer_activated)

    def setModel(self, model):
        self.filterModel.setSourceModel(model)
        super().setModel(self.filterModel)

    def filter(self, text):
        self.filterModel.setFilterFixedString(text)

    def on_completer_activated(self, text):
        if text:
            #index = self.findText(text)
            for i in range(self.count()):
                if text == self.itemText(i):
                    self.setCurrentIndex(i)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    combo = AutoComboBox()
    names = ['bob', 'fred', 'bobby', 'frederick', 'charles', 'charlie', 'rob']
    combo.addItems(names)
    combo.resize(300, 40)
    combo.show()
    sys.exit(app.exec_())