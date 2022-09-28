# custom qt window based on https://www.pythonfixing.com/2022/01/fixed-custom-titlebar-with-frame-in.html

import sys

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
    def __init__(self):
        super(MainWindow, self).__init__()
        self.layout = QVBoxLayout()
        self.layout.addWidget(DarkBar(self, title="test"))
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


class DarkBar(QWidget):
    """A custom dark title bar for a window, meant to replace the default windows titlebar"""
    # note QWidget functions don't use camelCase, don't change this

    def __init__(self, parent, title="", height=35, *args, **kwargs):
        """
        Args:
            parent (QWidget): The parent widget
            title (str): The title of the window
        """
        super(DarkBar, self).__init__(*args, **kwargs)
        self.parent = parent

        self._height = height

        self.layout = QHBoxLayout()
        self.title = QLabel()
        self.icon_layout = QHBoxLayout()
        self.title_text = QLabel(title)

        self.btn_close = QPushButton("🗙")
        self.btn_minimize = QPushButton("🗕")
        self.btn_maximize = QPushButton("🗖")
        self.btn_restore = QPushButton("🗗", )
        self.btn_restore.setVisible(False)

        self._style_buttons_svg()

        self._connect_buttons()
        self._styling(height)

        self.layout.addWidget(self.title)
        self.icon_layout.addStretch(-1)
        self.icon_layout.addWidget(self.title_text)
        self.icon_layout.addStretch(-1)
        self.icon_layout.addWidget(self.btn_minimize)
        self.icon_layout.addWidget(self.btn_maximize)
        self.icon_layout.addWidget(self.btn_restore)
        self.icon_layout.addWidget(self.btn_close)
        self.title.setLayout(self.icon_layout)

        self.setLayout(self.layout)

        # init mouse tracking
        self.start = QPoint(0, 0)
        self.pressing = False

    def _style_buttons_svg(self):
        data = {
            self.btn_close: r"C:\Program Files\Epic Games\UE_5.0\Engine\Content\Slate\Starship\CoreWidgets\Window\close.svg",
            self.btn_minimize: r"C:\Program Files\Epic Games\UE_5.0\Engine\Content\Slate\Starship\CoreWidgets\Window\minimize.svg",
            self.btn_maximize: r"C:\Program Files\Epic Games\UE_5.0\Engine\Content\Slate\Starship\CoreWidgets\Window\maximize.svg",
            self.btn_restore: r"C:\Program Files\Epic Games\UE_5.0\Engine\Content\Slate\Starship\CoreWidgets\Window\restore.svg",
            #TODO restore
        }
        for btn, icon_path in data.items():

            if not Path(icon_path).exists():
                # use text as backup
                continue

            # p = r"C:\Program Files\Epic Games\UE_5.0\Engine\Content\Slate\Starship\CoreWidgets\Window\close.svg"
            icon = QtGui.QIcon(icon_path)
            btn.setIcon(icon)
            btn.setIconSize(PySide2.QtCore.QSize(self._height, self._height))
            btn.setText("")  # clear text if we set icon


    def _connect_buttons(self):
        self.btn_close.clicked.connect(self.close_parent)
        self.btn_minimize.clicked.connect(self.minimize_parent)
        self.btn_maximize.clicked.connect(self.maximize_parent)
        self.btn_restore.clicked.connect(self.maximize_parent)

    def _styling(self, height):
        """prettify the qt elements, run after creating all elements in init"""

        # unreal dark grey
        ue_grey = "#151515"
        ue_grey_white = "#c0c0c0"

        # remove padding layout
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.icon_layout.setSpacing(0)
        self.icon_layout.setContentsMargins(0, 0, 0, 0)

        # style buttons
        for btn in [self.btn_close, self.btn_minimize, self.btn_maximize, self.btn_restore]:
            btn.setFixedSize(height, height)
            btn.setStyleSheet(f"background-color: transparent; font-size: 14px; color: {ue_grey_white};")
            btn.setFlat(True)  # remove frame from buttons

        # style title
        self.title.setFixedHeight(height)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet(f"""background-color: {ue_grey};""")
        self.title_text.setStyleSheet(f"""color: {ue_grey_white};""")


    # resizing is not implemented
    # def resizeEvent(self, QResizeEvent):
    #     super(MyBar, self).resizeEvent(QResizeEvent)
    #     self.title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

        window = self.parent.windowHandle()
        window.startSystemMove()

    def close_parent(self):
        self.parent.close()

    def maximize_parent(self):
        # modified this func to support going back to normal
        if self.parent.windowState() & PySide2.QtCore.Qt.WindowMaximized:
            self.parent.showNormal()
            self.btn_maximize.setVisible(True)
            self.btn_restore.setVisible(False)
        else:
            self.parent.showMaximized()
            self.btn_maximize.setVisible(False)
            self.btn_restore.setVisible(True)

    def minimize_parent(self):
        self.parent.showMinimized()


if not QApplication.instance():
    app = QApplication(sys.argv)
mw = MainWindow()
mw.show()

import unreal
unreal.parent_external_window_to_slate(mw.winId())

raise Exception("test")