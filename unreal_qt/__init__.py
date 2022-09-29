"""
Add support for qt in unreal without blocking the editor/tick
"""

import unreal
import sys

from PySide2 import QtWidgets, QtCore

# tick_handle = None
# existing_windows = {}
# opened_windows = []


# # This function will receive the tick from Unreal
# def __qt_app_tick(delta_seconds):
#     for window in opened_windows:
#         window.eventTick(delta_seconds)
#
#
# # This function will be called when the application is closing.
# def __qt_app_quit():
#     unreal.unregister_slate_post_tick_callback(tick_handle)
#
#
# # This function is called by the windows when they are closing. (Only if the connection is properly made.)
# def __qt_window_closed(window=None):
#     if window in opened_windows:
#         opened_windows.remove(window)


def setup():
    """This part is for the initial setup. Need to run once to spawn the application."""
    global tick_handle
    print("Start setup unreal_qt")

    # enable dpi scale, run before creating QApplication
    QtWidgets.QApplication.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

    unreal_app = QtWidgets.QApplication.instance() or QtWidgets.QApplication(sys.argv)
        # tick_handle = unreal.register_slate_post_tick_callback(__qt_app_tick)
        # unreal_app.aboutToQuit.connect(__qt_app_quit)
        # existing_windows = {}
        # opened_windows = []

    import unreal_qt.unrealStylesheet.main
    unreal_qt.unrealStylesheet.main.setup()

    print("Finished setup unreal_qt")


# based on https://github.com/AlexQuevillon/UnrealPythonLibrary
# def spawn_qt_window(desired_window_class=None):
#     """
#     desired_window_class: class QtGui.QWidget : The window class you want to spawn
#     return: The new or existing window
#     """
#     window = existing_windows.get(desired_window_class, None)
#     if not window:
#         window = desired_window_class()
#         existing_windows[desired_window_class] = window
#         window.aboutToClose = __qt_window_closed
#     if window not in opened_windows:
#         opened_windows.append(window)
#     window.show()
#     window.activateWindow()
#     return window
