#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from PyQt5.QtSql import *


class SqliteHelper:
    def __init__(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        file = os.path.join(os.path.dirname(__file__), "../wizemr.db")
        self.db.setDatabaseName(file)

    def open(self):
        if not self.db.isValid():
            return False
        if not self.db.isOpen():
            self.db.open()
            return True
        return True

    def close(self):
        if self.db.isValid():
            if self.db.isOpen():
                self.db.close()
