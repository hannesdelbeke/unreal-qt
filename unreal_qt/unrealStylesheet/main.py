import sys
import os

from PySide2 import QtWidgets, QtCore
from pathlib import Path


MODULE_PATH = Path(__file__).parent.resolve()
QSS_PATH = MODULE_PATH / 'ue.qss'


def setup():
    app = QtWidgets.QApplication.instance()
    if not app:
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        app = QtWidgets.QApplication(sys.argv)

    QtCore.QResource.registerResource(str(MODULE_PATH / "icons.rcc"))

    with open(QSS_PATH, 'r') as f:
        qss = f.read()
        app.setStyleSheet(qss)
