"""
Add support for qt in unreal without blocking the editor/tick
"""
import unreal
import unreal_stylesheet
import sys
try:
    from PySide6 import QtWidgets, QtCore
except ImportError:
    from PySide2 import QtWidgets, QtCore
# import functools
# import unreal_qt.dark_bar


__widgets = []
__excluded_widgets = []


def setup():
    """This part is for the initial setup. Need to run once to spawn the application."""
    print("Starting unreal_qt setup")

    # enable dpi scale, run before creating QApplication
    QtWidgets.QApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    unreal_app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
    unreal_stylesheet.setup()

    print("Completed unreal_qt setup")


# class widget_manager():
#     widgets = []
# 
#     @classmethod
#     def _wrap_closeEvent(cls, widget, original_closeEvent):  # noqa
#         def closeEvent(self, event):  # noqa
#             # run original closeEvent
#             result = original_closeEvent(event)
#             # remove widget from list
#             close_widget = event.isAccepted()
#             if close_widget:
#                 cls.remove_widget(self)
#             # return original result
#             return result
#         functools.partial(closeEvent, widget)
#         return closeEvent
# 
#     @classmethod
#     def _wrap_show(cls, widget):
#         original_show = widget.show
#         def show(self):
#             original_show()
#             unreal.parent_external_window_to_slate(widget.winId())  # this only works after showing the widget
#         functools.partial(show, widget)
# 
#     @classmethod
#     def add_widget(cls, widget: QtWidgets.QWidget):
#         """
#         Add a widget to the widget manager.
#         - prevent widget from being garbage collected
#         - hookup closeEvent to remove widget from manager
#         - add dark window bar to mimic Unreal's visual style
#         - parent widget to Unreal's main window to stay on top
#         """
#         if widget in cls.widgets:
#             return widget
#         widget = unreal_qt.dark_bar.wrap_widget_unreal(widget)
#         cls.widgets.append(widget)
#         cls._wrap_closeEvent(widget, widget.closeEvent)
#         cls._wrap_show(widget)
#         return widget

# This function is called by the windows when they are closing. (Only if the connection is properly made.)
# def __qt_window_closed(window=None):
#     if window in opened_windows:
#         opened_windows.remove(window)


class widget_manager():
    widgets = []

    @classmethod
    def add_widget(cls, widget: QtWidgets.QWidget):
        if widget in cls.widgets:
            return
        
        # connect a callback to the close event of the widget
        widget.close.connect(lambda: cls.remove_window(widget))

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

        unreal.parent_external_window_to_slate(widget.winId())

        __widgets.append(widget)
        unreal.log_warning(f"parented widget {widget}")


__timer = 0


def tick(delta_seconds):
    global __timer
    __timer += delta_seconds
    if __timer >= 0.3:
        parent_orphan_widgets()

# Example usage
# Assuming this is being executed in Unreal's Python environment
# You can hook up the tick method to Unreal's tick mechanism
setup()
unreal.register_slate_post_tick_callback(tick)  # Hook up to Unreal's tick mechanism
