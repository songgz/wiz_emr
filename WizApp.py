import sys
from PyQt5.QtWidgets import QApplication
from Wiz.MainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet("*{font-size:13px;}")
    # app.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))
    ex = MainWindow()
    ex.show()

    sys.exit(app.exec_())
