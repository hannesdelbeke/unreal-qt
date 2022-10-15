"""
qt sample with unreal_qt
"""

from PySide2.QtWidgets import QLabel, QWidget, QVBoxLayout

w = QWidget()
layout = QVBoxLayout()
w.setLayout(layout)
layout.addWidget(QLabel("Hello World!"))
w.show()
