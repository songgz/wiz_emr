from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from Wiz.Conn import *
from Wiz.DrugComboBox import *


class DBComboBoxDelegate(QItemDelegate):
    def __init__(self, parent=None):
        QItemDelegate.__init__(self, parent)
        self.itemModel = QtSql.QSqlQueryModel()
        self.itemModel.setQuery('select name, id, pinyin from drug')

    def createEditor(self, parent, option, proxyModelIndex):
        combo = DrugComboBox(parent)
        combo.setModel(self.itemModel)
        combo.setEditable(True)
        return combo

    def setEditorData(self, editor, index):
        value = index.data(Qt.DisplayRole)
        for i in range(editor.count()):
            if value == editor.model().index(i, 1).data(Qt.DisplayRole):
                editor.setCurrentIndex(i)
                break

    def setModelData(self, editor, model, index):
        model.setData(index, editor.model().index(editor.currentIndex(), 1).data(Qt.DisplayRole))
        pass

    def paint(self, painter, option, index):
        value = index.data(Qt.DisplayRole)
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
        str = ''
        for i in range(self.itemModel.rowCount()):
            rec = self.itemModel.record(i)
            if rec.value('id') == value:
                str = rec.value('name')
                break
        painter.drawText(option.rect, Qt.AlignLeft | Qt.AlignVCenter, str)


class SpinDelegate(QItemDelegate):
    def __init__(self):
        super(SpinDelegate, self).__init__()
        pass

    def createEditor(self, parent, QStyleOptionViewItem, QModelIndex):
        editor = QSpinBox(parent)
        editor.installEventFilter(self)
        editor.setMinimum(0)
        editor.setMaximum(1000)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        editor.setValue(value)

    def setModelData(self, editor, model, index):
        value = editor.value()
        model.setData(index, value, Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class MedicalRecord(QWidget):
    def __init__(self):
        super().__init__()
        self.patient_id = 0
        self.appointment_id = 0
        self.appointment_size = 0
        self.appointment_index = 0
        self.appointment = QtSql.QSqlTableModel()
        self.appointment.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        self.appointment.setTable('appointment')
        self.appointment.setFilter("patient_id={0}".format(self.patient_id))
        self.name = QLineEdit()
        self.gender = QComboBox()
        self.gender.addItem('女', 0)
        self.gender.addItem('男', 1)
        self.age = QSpinBox()
        self.age.setRange(0, 130)
        self.age.setValue(35)
        self.address = QLineEdit()
        self.symptom = QTextEdit()
        self.symptom.setMaximumHeight(80)
        self.diagnosis = QLineEdit()
        self.note = QTextEdit()
        self.note.setMaximumHeight(80)
        self.times = QLabel()
        self.created_at = QDateEdit()
        self.created_at.setDate(QDate.currentDate())
        self.no_code = QLineEdit()
        self.tel = QLineEdit()
        self.dosages = QSpinBox()

        self.prescription = QtSql.QSqlRelationalTableModel()
        self.prescription.setTable("prescription")
        self.prescription.setEditStrategy(QtSql.QSqlTableModel.OnManualSubmit)
        #self.prescription.setRelation(1, QtSql.QSqlRelation('drug', 'id', 'name'))

        self.prescription.setHeaderData(0, Qt.Horizontal, QVariant("ID"))
        self.prescription.setHeaderData(1, Qt.Horizontal, QVariant("药品"))
        self.prescription.setHeaderData(2, Qt.Horizontal, QVariant("药量"))
        self.prescription.setHeaderData(3, Qt.Horizontal, QVariant("备注"))
        self.prescription.setFilter("appointment_id={0}".format(self.appointment_id))
        self.prescription.select()
        self.table = QTableView()
        self.menu = QMenu()
        self.insertAct = QAction(QIcon(':/images/data_add.png'), '&添加药品', self)
        self.insertAct.triggered.connect(self.add_drug)
        self.delAct = QAction(QIcon(':/images/data_delete.png'), '删除药品', self)
        self.delAct.triggered.connect(self.del_drug)
        self.menu.addAction(self.insertAct)
        self.menu.addAction(self.delAct)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        pr0 = QHBoxLayout()
        pr0.addWidget(QLabel('日期：'))
        pr0.addWidget(self.created_at)
        pr0.addWidget(QLabel('病历号：'))
        pr0.addWidget(self.no_code)

        pr0.addWidget(QLabel('诊次：'))
        pr0.addWidget(self.times)
        layout.addLayout(pr0)
        pr1 = QHBoxLayout()
        pr1.addWidget(QLabel('姓名：'))
        pr1.addWidget(self.name)
        pr1.addWidget(QLabel('性别：'))
        pr1.addWidget(self.gender)
        pr1.addWidget(QLabel('年龄：'))
        pr1.addWidget(self.age)
        pr2 = QHBoxLayout()
        pr2.addWidget(QLabel('住址：'))
        pr2.addWidget(self.address)
        pr2.addWidget(QLabel('电话：'))
        pr2.addWidget(self.tel)
        layout.addLayout(pr1)
        layout.addLayout(pr2)
        r1 = QHBoxLayout()
        r1.addWidget(QLabel('症状：'))
        self.symptom.resize(self.symptom.width(), 30)
        r1.addWidget(self.symptom)
        layout.addLayout(r1)
        r2 = QHBoxLayout()
        r2.addWidget(QLabel('诊断：'))
        r2.addWidget(self.diagnosis)
        layout.addLayout(r2)
        r3 = QHBoxLayout()
        r3.addWidget(QLabel('处方：'))
        r3.addWidget(self.table)
        layout.addLayout(r3)
        r31 = QHBoxLayout()
        r31.addWidget(QLabel('剂数：'))
        r31.addWidget(self.dosages)
        layout.addLayout(r31)
        r4 = QHBoxLayout()
        r4.addWidget(QLabel('备注：'))
        r4.addWidget(self.note)
        layout.addLayout(r4)
        self.table.setModel(self.prescription)
        #self.table.setItemDelegate(QtSql.QSqlRelationalDelegate(self))
        self.table.setSelectionMode(QTableView.SingleSelection)
        self.table.setSelectionBehavior(QTableView.SelectRows)
        self.table.resizeColumnsToContents()
        #self.table.resizeColumnToContents(1)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setColumnHidden(0, True)
        self.table.setColumnHidden(4, True)

        self.table.setItemDelegateForColumn(1, DBComboBoxDelegate(self.table))
        self.table.setItemDelegateForColumn(2, SpinDelegate())
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_menu)

        self.setLayout(layout)

    def new_pq(self):
        self.appointment_index = self.appointment_size = 0
        self.patient_id = 0
        self.name.setText('')
        self.gender.setCurrentIndex(0)
        self.age.setValue(30)
        self.address.setText('')
        self.tel.setText('')
        self.new_mr()

    def new_mr(self):
        self.appointment_id = 0
        self.symptom.setText('')
        self.diagnosis.setText('')
        self.created_at.setDate(QDate.currentDate())
        self.dosages.setValue(1)
        self.note.setText('')
        self.prescription.setFilter("appointment_id={0}".format(self.appointment_id))

    def save_mr(self):
        if self.patient_id > 0:
            self.edit_patient()
        else:
            self.add_patient()

        if self.appointment_id > 0:
            self.edit_appointment()
            self.prescription.submitAll()
        else:
            self.add_appointment()
            self.add_prescription()

    def delete_mr(self):
        reply = QMessageBox.information(self,  "删除", "确定删除此病历吗？", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.appointment.removeRow(self.appointment_index - 1)
            self.appointment.submitAll()
            self.prescription.removeRows(0, self.prescription.rowCount())
            self.prescription.submitAll()
            self.appointment_index = self.appointment_size = self.appointment.rowCount()
            self.load_mr(self.appointment_index)
            self.times.setText("{0}/{1}".format(self.appointment_index, self.appointment_size))

    def remove_pq(self):
        reply = QMessageBox.information(self, "删除", "确定删除此患者及其病历吗？", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            q = QtSql.QSqlQuery()
            q.exec_("DELETE FROM prescription WHERE appointment_id IN (SELECT id FROM appointment WHERE patient_id={0})".format(self.patient_id))
            self.appointment.removeRows(0, self.appointment.rowCount())
            self.appointment.submitAll()
            pq = self.parent().ps
            pq.delete_pq()
            self.new_pq()
            self.times.setText("{0}/{1}".format(self.appointment_index, self.appointment_size))

    def add_patient(self):
        pq = self.parent().ps
        num = pq.model.rowCount()
        record = pq.model.record()
        record.setValue('name', self.name.text())
        record.setValue('gender', self.gender.currentData())
        record.setValue('age', self.age.value())
        record.setValue('address', self.address.text())
        record.setValue('tel', self.tel.text())
        record.setValue('created_at', QDate.currentDate())
        record.setValue('updated_at', self.created_at.date())
        pq.model.insertRecord(num, record)
        pq.model.submitAll()
        record = pq.model.record(num)
        self.patient_id = record.value('id')
        print(self.patient_id)

    def edit_patient(self):
        pq = self.parent().ps
        num = pq.table.currentIndex().row()
        record = pq.model.record(num)
        record.setValue('name', self.name.text())
        record.setValue('gender', self.gender.currentData())
        record.setValue('age', self.age.value())
        record.setValue('address', self.address.text())
        record.setValue('tel', self.tel.text())
        record.setValue('updated_at', self.created_at.date())
        pq.model.setRecord(num, record)
        pq.model.submitAll()

    def add_appointment(self):
        self.appointment.setFilter("patient_id={0}".format(self.patient_id))
        num = self.appointment.rowCount()
        record = self.appointment.record()
        record.setValue('patient_id', self.patient_id)
        record.setValue('symptom', self.symptom.toPlainText())
        record.setValue('diagnosis', self.diagnosis.text())
        record.setValue('note', self.note.toPlainText())
        record.setValue('dosages', self.dosages.value())
        record.setValue('created_at', self.created_at.text())
        self.appointment.insertRecord(num, record)
        self.appointment.submitAll()
        r = self.appointment.record(num)
        self.appointment_id = r.value('id')
        print(self.appointment_id)
        self.appointment_index = self.appointment_size = self.appointment.rowCount()
        self.times.setText("{0}/{1}".format(self.appointment_index, self.appointment_size))

    def edit_appointment(self):
        num = self.appointment_index - 1
        record = self.appointment.record(num)
        record.setValue('symptom', self.symptom.toPlainText())
        record.setValue('diagnosis', self.diagnosis.text())
        record.setValue('note', self.note.toPlainText())
        record.setValue('dosages', self.dosages.value())
        record.setValue('created_at', self.created_at.text())
        self.appointment.setRecord(num, record)
        self.appointment.submitAll()

    def add_prescription(self):
        for i in range(self.prescription.rowCount()):
            rec = self.prescription.record(i)
            rec.setValue('appointment_id', self.appointment_id)
            self.prescription.setRecord(i, rec)
        self.prescription.submitAll()
        self.prescription.setFilter("appointment_id={0}".format(self.appointment_id))

    def change_patient(self, record):
        self.patient_id = record.value('id')
        self.name.setText(record.value('name'))
        self.gender.setCurrentIndex(record.value('gender'))
        self.age.setValue(record.value('age'))
        self.address.setText(record.value('address'))
        self.tel.setText(record.value('tel'))
        self.appointment.setFilter("patient_id={0}".format(self.patient_id))
        self.appointment.select()
        self.appointment_index = self.appointment_size = self.appointment.rowCount()
        if self.appointment_size > 0:
            self.load_mr(self.appointment_index)
        else:
            self.new_mr()
        self.times.setText("{0}/{1}".format(self.appointment_index, self.appointment_size))

    def load_mr(self, index):
        record = self.appointment.record(index - 1)
        self.appointment_id = record.value('id')
        self.symptom.setText(record.value('symptom'))
        self.diagnosis.setText(record.value('diagnosis'))
        self.note.setText(record.value('note'))
        self.dosages.setValue(record.value('dosages'))
        self.created_at.setDate(QDate.fromString(record.value('created_at'), 'yyyy-MM-dd'))
        self.prescription.setFilter("appointment_id={0}".format(record.value('id')))
        self.prescription.select()

    def next(self):
        if self.appointment_size > 0 and self.appointment_index > 1:
            self.appointment_index -= 1
            self.load_mr(self.appointment_index)
            self.times.setText("{0}/{1}".format(self.appointment_index, self.appointment_size))

    def prev(self):
        if self.appointment_size > 0 and self.appointment_size > self.appointment_index:
            self.appointment_index += 1
            self.load_mr(self.appointment_index)
            self.times.setText("{0}/{1}".format(self.appointment_index, self.appointment_size))

    def open_menu(self, pos):
        action = self.menu.exec_(self.table.mapToGlobal(pos))
        # if action == self.insertAct:
        #     r = self.prescription.record()
        #     r.setValue('appointment_id', self.appointment_id)
        #     self.prescription.insertRecord(self.prescription.rowCount(), r)
        # if action == self.delAct:
        #     self.prescription.removeRow(self.table.currentIndex().row())
        pass

    def add_drug(self):
        r = self.prescription.record()
        r.setValue('appointment_id', self.appointment_id)
        self.prescription.insertRecord(self.prescription.rowCount(), r)

    def del_drug(self):
        self.prescription.removeRow(self.table.currentIndex().row())



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    combo = DrugComboBox()
    names = ['bob', 'fred', 'bobby', 'frederick', 'charles', 'charlie', 'rob']
    #combo.addItems(names)
    drug = QtSql.QSqlQueryModel()
    drug.setQuery('select name, id, pinyin from drug')
    combo.setModel(drug)
    combo.resize(300, 40)
    combo.show()
    sys.exit(app.exec_())
