"""
Add support for qt in unreal without blocking the editor/tick
"""
import unreal_qt.unrealStylesheet.main
import sys
from PySide2 import QtWidgets, QtCore
import functools
import unreal_qt.dark_bar
import unreal


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


class widget_manager():
    widgets = []

    @classmethod
    def _wrap_closeEvent(cls, widget, original_closeEvent):  # noqa
        def closeEvent(self, event):  # noqa
            # run original closeEvent
            result = original_closeEvent(event)
            # remove widget from list
            close_widget = event.isAccepted()
            if close_widget:
                cls.remove_widget(self)
            # return original result
            return result
        functools.partial(closeEvent, widget)
        return closeEvent

    @classmethod
    def _wrap_show(cls, widget):
        original_show = widget.show
        def show(self):
            original_show()
            unreal.parent_external_window_to_slate(widget.winId())  # this only works after showing the widget
        functools.partial(show, widget)

    @classmethod
    def add_widget(cls, widget: QtWidgets.QWidget):
        """
        Add a widget to the widget manager.
        - prevent widget from being garbage collected
        - hookup closeEvent to remove widget from manager
        - add dark window bar to mimic Unreal's visual style
        - parent widget to Unreal's main window to stay on top
        """
        if widget in cls.widgets:
            return widget
        widget = unreal_qt.dark_bar.wrap_widget_unreal(widget)
        cls.widgets.append(widget)
        cls._wrap_closeEvent(widget, widget.closeEvent)
        cls._wrap_show(widget)
        return widget

    @classmethod
    def remove_widget(cls, widget):
        cls.widgets.remove(widget)


def wrap(widget):
    return widget_manager.add_widget(widget)
