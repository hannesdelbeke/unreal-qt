"""
Add support for qt in unreal without blocking the editor/tick
"""
import unreal
import unreal_stylesheet
import sys

from PySide6 import QtWidgets, QtCore
print("unreal_qt setup PySide6")

# import functools
# import unreal_qt.dark_bar


__widgets = []
__excluded_widgets = []
__tick_handler = None


def setup():
    """This part is for the initial setup. Need to run once to spawn the application."""
    print("Starting unreal_qt setup")

    # enable dpi scale, run before creating QApplication
    QtWidgets.QApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    #QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    #QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    unreal_app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
    unreal_stylesheet.setup()

    global __tick_handler

    if __tick_handler is None:
        __tick_handler = unreal.register_slate_post_tick_callback(tick)  # Hook up to Unreal's tick mechanism

    print("Completed unreal_qt setup")


class widget_manager():
    widgets = []

    @classmethod
    def add_widget(cls, widget: QtWidgets.QWidget):
        if widget in cls.widgets:
            return
        
        # connect a callback to the close event of the widget
        widget.destroyed.connect(lambda: cls.remove_widget(widget))

        cls.widgets.append(widget)

    @classmethod
    def remove_widget(cls, widget):
        print("remove_window")
        cls.widgets.remove(widget)


def wrap(widget):
    return widget_manager.add_widget(widget)



def _orphan_toplevel_widgets():
    return [widget for widget in QtWidgets.QApplication.instance().topLevelWidgets() if
            not widget.parent()
            and widget not in __widgets
            and widget not in __excluded_widgets]


def parent_orphan_widgets(exclude=None):
    """Find and parent orphan widgets to the Unreal widget"""
    # this runs every frame, don't print or log in this method
    exclude = exclude or []
    __excluded_widgets.extend(exclude)
    for widget in _orphan_toplevel_widgets():
        if widget.windowType() in (QtCore.Qt.WindowType.ToolTip, ):
            __excluded_widgets.append(widget)
            continue
        elif not widget.windowType() in (QtCore.Qt.Window, QtCore.Qt.Dialog, ):
            unreal.log_warning(f"Skipping widget: '{widget}' not window type but {widget.windowType()}")
            __excluded_widgets.append(widget)
            continue

        searchmethod = unreal.SlateParentWindowSearchMethod.MAIN_WINDOW
        unreal.parent_external_window_to_slate(widget.winId(), searchmethod)

        __widgets.append(widget)
        unreal.log_warning(f"parented widget {widget}")


__timer = 0

def tick(delta_seconds):
    global __timer
    __timer += delta_seconds
    if __timer >= 0.3:
        parent_orphan_widgets()
