"""
an icon browser for the unreal engine project resources
"""
# import QWidget
from PySide2 import QtWidgets, QtCore, QtGui, QtUiTools
from PySide2.QtWidgets import QApplication, QLabel, QDialog, QWidget
from pathlib import Path


# create a widget showing all icons in the icon folder
class IconWidget(QWidget):
    def __init__(self, *args):
        super(IconWidget, self).__init__(*args)

        # get icons
        content_path = Path(r"C:\Program Files\Epic Games\UE_5.0\Engine\Content\\")
        # search for all pngs recursively
            # for every icon in glob
            # create a label with the icon
            # add the label to the layout
            # self.layout.addWidget(label)
        layout = QtWidgets.QVBoxLayout(self)

        #' tabs
        self.tab_widget = QtWidgets.QTabWidget()
        image_types = ["png", "bmp", "svg", "tps", "ttf"]

        self.lists = []
        for img_type in image_types:

            thumbnail_list = QtWidgets.QListWidget(self)
            thumbnail_list.setResizeMode(QtWidgets.QListWidget.Adjust)
            if img_type not in ["tps", "ttf"]:
                thumbnail_list.setViewMode(QtWidgets.QListView.IconMode)
                thumbnail_list.setIconSize(QtCore.QSize(64, 64))
            # set background to dark grey, text to white
            # thumbnail_list.setStyleSheet("background-color: rgb(50, 50, 50); color: rgb(255, 255, 255);")
            thumbnail_list.setDragEnabled(False)

            self.lists.append(thumbnail_list)

            icon_paths = content_path.glob(f"**/*.{img_type}")
            icon_count = 0
            for thumbnail_path in icon_paths:
                icon = QtGui.QIcon(str(thumbnail_path))
                name = ""
                if img_type in ["tps", "ttf"]:
                    name = thumbnail_path.stem
                item = QtWidgets.QListWidgetItem(icon, name)
                # set tooltip to path
                item.setToolTip(str(thumbnail_path))
                # item.setData(QtCore.Qt.UserRole, file_path)
                thumbnail_list.addItem(item)
                icon_count += 1

            if icon_count == 0:
                print(f"no icons found for {img_type}")
                continue

            tab = QtWidgets.QWidget()
            tab.layout = QtWidgets.QVBoxLayout()
            tab.setLayout(tab.layout)

            tab.layout.addWidget(thumbnail_list)

            self.tab_widget.addTab(tab, f"{img_type}({icon_count})")

            # connect click
            thumbnail_list.itemClicked.connect(self.click_icon)

            # connect tab change
            self.tab_widget.currentChanged.connect(self.search_current_tab)
            # thumbnail_list.itemClicked.connect(self.search_current_tab)


        # textfield to search for icons
        self.search_field = QtWidgets.QLineEdit()
        self.search_field.textChanged.connect(self.search)
        layout.addWidget(self.search_field)
        self.setLayout(layout)
        layout.addWidget(self.tab_widget)

        self.selected_field = QtWidgets.QLineEdit()
        layout.addWidget(self.selected_field)

    def search_current_tab(self, index):
        # get tab from index
        tab = self.tab_widget.widget(index)
        self._search(self.search_field.text(), tab)

    def search(self, text=None):

        # if text is none, we redo the same search but on the current tab
        if text is None:
            text = self.search_field.text()

        # get active tab
        active_tab = self.tab_widget.currentWidget()
        self._search(text, active_tab)

    def _search(self, text, tab):
        # get list
        active_list = tab.layout.itemAt(0).widget()

        for i in range(active_list.count()):
            item = active_list.item(i)
            if text.lower() in item.toolTip().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)

    def click_icon(self, item):
        self.selected_field.setText(item.toolTip())


window = None

def show():
    # app = QApplication([])
    global window
    window = IconWidget()
    window.resize(1000, 800)
    window.show()

    import unreal
    unreal.parent_external_window_to_slate(window.winId())
    # app.exec_()
