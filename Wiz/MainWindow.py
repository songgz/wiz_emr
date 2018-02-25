#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from Wiz.DrugDialog import DrugDialog
from Wiz.MedicalRecord import MedicalRecord
from Wiz.PatientQuery import PatientQuery
from rcc import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.drug = DrugDialog()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowIcon(QIcon(':/images/klipper.png'))
        #self.setToolTip('看什么看^_^')
        #QToolTip.setFont(QFont('微软雅黑', 12))

        #rp.setTitle('处方笺')
        #emr = MainPanel()
        self.mr = MedicalRecord()
        self.setCentralWidget(self.mr)

        self.ps = PatientQuery()
        #ps.setTitle('患者')
        doc = QDockWidget('患者', self)
        doc.setObjectName('DocLog')
        doc.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        doc.setWidget(self.ps)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, doc)

        self.resize(1080, 720)       
        
        exitAction = QAction(QIcon(':images/system-shutdown.png'), '&退出', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('退出')
        #exitAction.triggered.connect(self.close)
        exitAction.triggered.connect(qApp.quit)

        saveAction = QAction(QIcon(':/images/save.png'), '&保存', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('保存')
        # exitAction.triggered.connect(self.close)
        saveAction.triggered.connect(self.mr.save_mr)

        newAction = QAction(QIcon(':/images/appointment-new.png'), '&复诊', self)
        newAction.setStatusTip('复诊病历')
        newAction.triggered.connect(self.mr.new_mr)

        patientAction = QAction(QIcon(':/images/user_add.png'), '&初诊', self)
        patientAction.setStatusTip('初诊病历')
        patientAction.triggered.connect(self.mr.new_pq)

        deleteAction = QAction(QIcon(':/images/appointment-delete.png'), '&删除病历', self)
        deleteAction.setStatusTip('删除病历')
        deleteAction.triggered.connect(self.mr.delete_mr)

        removeAction = QAction(QIcon(':/images/user_remove.png'), '&删除患者', self)
        removeAction.setStatusTip('删除患者')
        removeAction.triggered.connect(self.mr.remove_pq)

        nextAction = QAction(QIcon(':/images/go-previous-view-page.png'), '&前诊', self)
        nextAction.setStatusTip('前一病历')
        nextAction.triggered.connect(self.mr.next)

        prevAction = QAction(QIcon(':/images/go-next-view-page.png'), '&后诊', self)
        prevAction.setStatusTip('后一病历')
        prevAction.triggered.connect(self.mr.prev)

        drugAction = QAction(QIcon(':/images/order.png'), '&药品', self)
        drugAction.setStatusTip('管理药物')
        drugAction.triggered.connect(self.open_drug)

        aboutAction = QAction(QIcon(':/images/klipper.png'), '&关于', self)
        aboutAction.setStatusTip('关于我们')
        aboutAction.triggered.connect(self.open_about)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&文件')
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)
        editMenu = menubar.addMenu('&病历')
        editMenu.addAction(patientAction)
        editMenu.addAction(newAction)
        editMenu.addAction(nextAction)
        editMenu.addAction(prevAction)
        editMenu.addAction(deleteAction)
        editMenu.addAction(removeAction)
        mgrMenu = menubar.addMenu('&管理')
        mgrMenu.addAction(drugAction)
        helpMenu = menubar.addMenu('&帮助')
        helpMenu.addAction(aboutAction)

        toolbar = self.addToolBar('Edit')
        toolbar.addAction(saveAction)
        toolbar.addAction(patientAction)
        toolbar.addAction(newAction)
        toolbar.addAction(nextAction)
        toolbar.addAction(prevAction)
        toolbar.addAction(deleteAction)
        toolbar.addAction(removeAction)
        toolbar.addAction(self.mr.insertAct)
        toolbar.addAction(self.mr.delAct)
        self.statusBar().showMessage('Ready')
        
        #self.setGeometry(300, 300, 1080, 720)
        self.setWindowTitle('WizRp')
        #self.loadStyleSheet()
        #self.show()

    def loadStyleSheet(self):
        file = QFile(':/theme/default.qss')
        if file.exists():
            file.open(QFile.ReadOnly | QFile.Text)
            #self.setStyleSheet(QTextStream(file).readAll())
            qApp.setStyleSheet(QTextStream(file).readAll())

    def open_drug(self):
        self.drug.show()
        pass

    def open_about(self):
        QMessageBox.about(self, "关于",'病历管理软件\n Ver 1.10')
