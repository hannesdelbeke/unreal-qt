import sys
import os

from PySide2 import QtWidgets, QtCore, QtGui, QtUiTools
# from PySide2 import _loadUi


MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
UI_PATH = os.path.join(MODULE_PATH, 'ui', 'progress.ui')
QSS_PATH = os.path.join(MODULE_PATH, 'ue.qss')

# if __name__ == '__main__':
def setup():
    app = QtWidgets.QApplication.instance()
    if not app:
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        app = QtWidgets.QApplication(sys.argv)

    QtCore.QResource.registerResource("icons.rcc")

    with open(QSS_PATH, 'r') as f:
        qss = f.read()
        app.setStyleSheet(qss)

    window = QtWidgets.QMainWindow()
    QtUiTools.QUiLoader().load(UI_PATH, window)  # _loadUi(UI_PATH, window)
    window.show()
    # sys.exit(app.exec_())
