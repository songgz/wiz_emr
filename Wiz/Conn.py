import os
from PyQt5 import QtSql

db=QtSql.QSqlDatabase.addDatabase("QSQLITE")
file = os.path.join(os.path.dirname(__file__),"../wizemr.db")
db.setDatabaseName(file)
ok=db.open()