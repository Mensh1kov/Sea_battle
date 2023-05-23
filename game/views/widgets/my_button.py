from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QWidget


class MyButton(QPushButton):
    def __init__(self, height: int, font_size: int,
                 text: str, widget: QWidget = None):
        super().__init__(text, widget)
        self.setFont(QFont(None, font_size))
        self.setMinimumSize(QtCore.QSize(0, height))
