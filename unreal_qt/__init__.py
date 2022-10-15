"""
Add support for qt in unreal without blocking the editor/tick
"""
import unreal_qt.unrealStylesheet.main
import sys
from PySide2 import QtWidgets, QtCore


def setup():
    """This part is for the initial setup. Need to run once to spawn the application."""
    print("Starting unreal_qt setup")

    # enable dpi scale, run before creating QApplication
    QtWidgets.QApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    unreal_app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
    unreal_qt.unrealStylesheet.main.setup()

    print("Completed unreal_qt setup")
