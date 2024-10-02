from PyQt5 import QtGui, QtWidgets
import sys
from mainWindow import Ui_MainWindow


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(r"images/icon.png"))
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())