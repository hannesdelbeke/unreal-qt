
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
        self.title_text = QLabel("   " + title)  # hack, add space instead of margin

        self.btn_close = QPushButton("🗙")
        self.btn_minimize = QPushButton("🗕")
        self.btn_maximize = QPushButton("🗖")
        self.btn_restore = QPushButton("🗗", )
        self.btn_restore.setVisible(False)

        # self._style_buttons_svg()

        self._connect_buttons()
        self._styling(height)

        self.layout.addWidget(self.title)
        # self.icon_layout.addStretch(-1)
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
        # set padding

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


class DarkBarUnreal(DarkBar):
    def __init__(self, parent, title="", height=35, *args, **kwargs):
        super(DarkBarUnreal, self).__init__(parent, title, height, *args, **kwargs)
        self._style_buttons_svg()

    def _style_buttons_svg(self):
        import unreal  # import unreal here to avoid import error in other dccs
        engine_content = Path(unreal.Paths.engine_content_dir())
        data = {
            self.btn_close: engine_content / r"Slate\Starship\CoreWidgets\Window\close.svg",
            self.btn_minimize: engine_content / r"Slate\Starship\CoreWidgets\Window\minimize.svg",
            self.btn_maximize: engine_content / r"Slate\Starship\CoreWidgets\Window\maximize.svg",
            self.btn_restore: engine_content / r"Slate\Starship\CoreWidgets\Window\restore.svg",
        }
        for btn, icon_path in data.items():

            if not icon_path.exists():
                # use text as backup
                continue

            icon = QtGui.QIcon(str(icon_path))
            btn.setIcon(icon)
            btn.setIconSize(PySide2.QtCore.QSize(self._height, self._height))
            btn.setText("")  # clear text if we set icon


class FramelessWindow(QWidget):
    """
    A frameless window with a custom title bar.
    Devs can add their own widgets to self.content_layout
    """

    default_title_bar = DarkBar

    def __init__(self, parent=None, title="", title_bar=None, *args, **kwargs):
        """
        Args:
            parent: parent widget
            title: title of the window
            title_bar: custom title bar instance, if None, use self.default_title_bar()
        """
        super().__init__(parent=parent, *args, **kwargs)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.title_bar = self._set_title_bar(title_bar, title)
        self.content_layout = QVBoxLayout()

        layout.addWidget(self.title_bar)  # add title bar
        layout.addLayout(self.content_layout)
        layout.addStretch(-1)  # so the bar stays at top when scaling the window

        # use CustomizeWindowHint when you want to support resizing
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setWindowFlags(Qt.Tool | Qt.CustomizeWindowHint)
        # otherwise use MSWindowsFixedSizeDialogHint
        # self.setWindowFlags(Qt.Tool | Qt.MSWindowsFixedSizeDialogHint)
        # self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)

    def _set_title_bar(self, title_bar, title):
        if not title_bar:
            title_bar = self.default_title_bar(self, title=title)
        return title_bar

    def setCentralWidget(self, widget):  # noqa: use same name convention as qmainwindow
        """add a widget to the content layout"""
        self.content_layout.addWidget(widget)
        return widget

    def setWindowTitle(self, title):
        self.title_bar.title_text.setText(title)


class FramelessWindowUnreal(FramelessWindow):
    default_title_bar = DarkBarUnreal


def wrap_widget_unreal(widget):
    """wrap a widget in a frameless window with a custom title bar"""
    # wrap widget in a frameless window
    window = FramelessWindowUnreal()
    window.setCentralWidget(widget)

    # copy over settings from widget
    window.setWindowTitle(widget.windowTitle())
    window.resize(widget.size())
    window.move(widget.pos())

    return window