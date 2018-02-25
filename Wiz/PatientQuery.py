from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Wiz.Conn import *


class DateFormatDelegate(QStyledItemDelegate):
    def __init__(self, date_format):
        QStyledItemDelegate.__init__(self)

    def displayText(self, value, locale):
        d = QDateTime.fromString(value, "yyyy-MM-ddThh:mm:ss.zzz")
        return d.toString("yyyy-MM-dd")


class GenderDelegate(QStyledItemDelegate):
    def displayText(self, value, locale):
        str = '男'
        if value == 0:
            str = '女'
        return str


class PatientQuery(QWidget):
    def __init__(self):
        super().__init__()
        self.model = QtSql.QSqlTableModel()
        self.model.setTable("patient")
        self.model.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.model.select()
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "患者姓名")
        self.model.setHeaderData(2, Qt.Horizontal, "性别")
        self.model.setHeaderData(3, Qt.Horizontal, "年龄")
        self.model.setHeaderData(4, Qt.Horizontal, "电话")
        self.model.setHeaderData(5, Qt.Horizontal, "病历号")
        self.model.setHeaderData(8, Qt.Horizontal, "日期")
        self.keyword = QLineEdit()
        self.search = QPushButton('搜索')
        self.deadline = QComboBox()
        self.deadline.addItem('今日', 1)
        self.deadline.addItem('本周', 2)
        self.deadline.addItem('本月', 3)
        self.deadline.addItem('全部', 0)
        self.table = QTableView()
        self.init_ui()

    def init_ui(self):
        r1 = QHBoxLayout()
        r1.addWidget(self.deadline)
        r1.addWidget(self.keyword)
        r1.addWidget(self.search)
        self.table.setModel(self.model)
        self.table.setItemDelegate(QtSql.QSqlRelationalDelegate(self.table))
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)
        #self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setColumnHidden(0, True)
        self.table.setColumnHidden(5, True)
        self.table.setColumnHidden(6, True)
        self.table.setColumnHidden(7, True)
        self.table.setItemDelegateForColumn(2, GenderDelegate(self))
        #self.table.setItemDelegateForColumn(8, DateFormatDelegate(self))
        self.table.doubleClicked.connect(self.double_click_enter)
        layout = QVBoxLayout()
        layout.addLayout(r1)
        layout.addWidget(self.table)
        self.setLayout(layout)
        self.search.clicked.connect(self.search_click)

    def search_options(self):
        index = self.deadline.currentData(Qt.UserRole)
        sql = "(name LIKE '%" + self.keyword.text() + "%' OR tel LIKE '%" + self.keyword.text() + "%')"
        if index == 1:
            sql += " and updated_at >=date('now','start of day')"
        elif index == 2:
            sql += " and updated_at >=date('now','-7 days')"
        elif index == 3:
            sql += " and updated_at >=date('now','-31 days')"
        else:
            sql += ''
        return sql

    def search_click(self):
        self.model.setFilter(self.search_options())

    def double_click_enter(self,index):
        rp = self.parent().parent().mr
        record = self.model.record(index.row())
        rp.change_patient(record)
        pass

    def delete_pq(self):
        self.model.removeRow(self.table.currentIndex().row())
        self.model.submitAll()
