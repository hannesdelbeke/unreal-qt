import sys
import os

from PySide2 import QtWidgets, QtCore


MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
UI_PATH = os.path.join(MODULE_PATH, 'ui', 'editor.ui')
QSS_PATH = os.path.join(MODULE_PATH, 'ue.qss')


def setup():
    app = QtWidgets.QApplication.instance()
    if not app:
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        app = QtWidgets.QApplication(sys.argv)

    QtCore.QResource.registerResource("icons.rcc")

    with open(QSS_PATH, 'r') as f:
        qss = f.read()
        app.setStyleSheet(qss)
