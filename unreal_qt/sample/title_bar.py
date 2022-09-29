# custom qt window based on https://www.pythonfixing.com/2022/01/fixed-custom-titlebar-with-frame-in.html

import sys
import unreal_qt.dark_bar
DarkBar = unreal_qt.dark_bar.DarkBarUnreal

# from PyQt5.QtCore import QPoint
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtWidgets import QHBoxLayout
# from PyQt5.QtWidgets import QLabel
# from PyQt5.QtWidgets import QPushButton
# from PyQt5.QtWidgets import QVBoxLayout
# from PyQt5.QtWidgets import QWidget
import PySide2.QtCore
import PySide2.QtGui as QtGui
from PySide2.QtCore import QPoint
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QHBoxLayout
from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QFrame, QDialog, QTabWidget
from pathlib import Path

# # https://stackoverflow.com/questions/7351493/how-to-add-border-around-qwidget
# class CentralWidget(QtGui.QFrame):
#     def __init__(self, *args):
#         super(CentralWidget, self).__init__(*args)
#         self.setStyleSheet("background-color: rgb(255,0,0); margin:5px; border:1px solid rgb(0, 255, 0); ")


def create_test_content(self):
    # test content
    self.button_test_content = QPushButton("hello_world")
    # self.layout.addWidget(self.btn_close)
    label = QLabel("this is a test")
    # label.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
    # label.setLineWidth(20)
    self.layout.addWidget(label)

    # TODO change tab spacing
    # TODO hover should be white text, non hover for active tab should be light grey text
    # TODO when tabs dont fit compact them instead of scroll arrows
    # create test tabs
    self.tab_widget = QTabWidget()
    self.tab_widget.addTab(QWidget(), "Tab 1")
    self.tab_widget.addTab(QWidget(), "Tab 2")
    self.tab_widget.addTab(QWidget(), "Tab 3")


class MainWindow(QWidget):
    def __init__(self, parent=None, title="",  *args, **kwargs):
        super(MainWindow, self).__init__(parent=None, *args, **kwargs)
        self.layout = QVBoxLayout()
        self.layout.addWidget(DarkBar(self, title=title))
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setMinimumSize(100,50)
        # self.pressing = False

        # use CustomizeWindowHint when you want to support resizing
        self.setWindowFlags(Qt.Tool | Qt.CustomizeWindowHint)
        # otherwise use MSWindowsFixedSizeDialogHint
        # self.setWindowFlags(Qt.Tool | Qt.MSWindowsFixedSizeDialogHint)
        # self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)

        create_test_content(self)

        self.layout.addStretch(-1)  # this helps the bar staying at top when scaling the window




if not QApplication.instance():
    app = QApplication(sys.argv)
mw = MainWindow(title="Game Exporter")
mw.show()

import unreal
unreal.parent_external_window_to_slate(mw.winId())

raise Exception("test")