from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Wiz.Conn import *


class DrugDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('药品管理')
        self.resize(640, 420)

        self.model = QtSql.QSqlTableModel()
        self.model.setTable("drug")
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "药品名称")
        self.model.setHeaderData(2, Qt.Horizontal, "拼音码")
        self.model.setHeaderData(3, Qt.Horizontal, "备注")
        self.model.select()
        self.table = QTableView()
        self.addBtn = QPushButton('新建')
        self.deleteBtn = QPushButton('删除')
        self.saveBtn = QPushButton('保存')
        self.init_ui()

    def init_ui(self):
        self.table.setModel(self.model)
        self.table.setItemDelegate(QtSql.QSqlRelationalDelegate(self.table))
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.resizeColumnsToContents()
        self.table.setColumnHidden(0, True)
        #self.table.setColumnHidden(3, True)
        self.table.setColumnHidden(4, True)
        self.table.setColumnHidden(5, True)
        self.table.setColumnHidden(6, True)
        self.table.horizontalHeader().setStretchLastSection(True)
        h = QHBoxLayout()
        h.addWidget(self.addBtn)
        h.addWidget(self.deleteBtn)
        h.addWidget(self.saveBtn)
        self.saveBtn.clicked.connect(self.save_drug)
        self.addBtn.clicked.connect(self.add_drug)
        self.deleteBtn.clicked.connect(self.del_drug)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(h)
        self.setLayout(layout)

    def save_drug(self):
        self.model.submitAll()

    def add_drug(self):
        self.model.insertRecord(self.model.rowCount(), self.model.record())
        pass

    def del_drug(self):
        self.model.removeRow(self.table.currentIndex().row())
        pass


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = DrugDialog()
    win.resize(640, 480)
    win.setWindowTitle('Drug')
    win.show()
    sys.exit(app.exec_())
    pass
