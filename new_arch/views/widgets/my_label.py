from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QWidget


class MyLabel(QLabel):
    def __init__(self, font_size: int, text: str, widget: QWidget = None):
        super().__init__(widget)
        self.setFont(QFont(None, font_size))
        self.setText(text)
        self.setAlignment(QtCore.Qt.AlignCenter)