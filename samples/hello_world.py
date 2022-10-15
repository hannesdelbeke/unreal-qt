"""
qt sample without unreal_qt
"""

import sys
from PySide2.QtWidgets import QApplication, QLabel


app = QApplication(sys.argv)  # This won't work if a QApplication already exists, e.g. if unreal_qt is setup
label = QLabel("Hello World!")
label.show()
app.exec_()  # this blocks the editor/tick in Unreal, it's not needed
