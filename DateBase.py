import os
from sqlobject import *
from datetime import *
sqlhub.processConnection = connectionForURI('sqlite:/'+os.path.join(os.path.dirname(__file__),"wizemr.db"))


class Patient(SQLObject):
    name = StringCol()
    age = IntCol()
    created_at = DateTimeCol()


class Drug(SQLObject):
    name = StringCol()
    in_stock = IntCol()
    sale_price = DecimalCol(size=10,precision=2)
    purchase_price = DecimalCol(size=10,precision=2)


if __name__ == '__main__':
    Patient.dropTable()
    Patient.createTable()

    p = Patient(name='tom', age=33, created_at=datetime(2016, 12, 22, 5, 2))
    p = Patient(name='scott', age=23, created_at=datetime(2016, 12, 21, 5, 2))
    p = Patient(name='scott', age=23, created_at=datetime(2016, 12, 1, 5, 2))

    Drug.dropTable()
    Drug.createTable()
    Drug(name='人参',in_stock=900, sale_price=9.00, purchase_price=7.00)
    Drug(name='白术', in_stock=900, sale_price=9.00, purchase_price=7.00)
    Drug(name='桂枝', in_stock=900, sale_price=9.00, purchase_price=7.00)

