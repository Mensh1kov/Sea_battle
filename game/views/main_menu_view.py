from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget


class MainMenuWidget(QWidget):
    def __init__(self, widget: QWidget = None):
        super().__init__(widget)
        self.resize(800, 500)
        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(220, 140, 351, 211))
        self.main_menu_buttons = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.main_menu_buttons.setContentsMargins(0, 0, 0, 0)
        font = QtGui.QFont()
        font.setPointSize(15)

        self.one_player_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.one_player_button.setMinimumSize(QtCore.QSize(0, 40))
        self.one_player_button.setFont(font)
        self.one_player_button.setText('One player')
        self.main_menu_buttons.addWidget(self.one_player_button)

        self.two_player_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.two_player_button.setMinimumSize(QtCore.QSize(0, 40))
        self.two_player_button.setFont(font)
        self.two_player_button.setText('Two player')
        self.main_menu_buttons.addWidget(self.two_player_button)

        self.settings_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.settings_button.setMinimumSize(QtCore.QSize(0, 40))
        self.settings_button.setFont(font)
        self.settings_button.setText('Settings')
        self.main_menu_buttons.addWidget(self.settings_button)

        self.exit_button = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.exit_button.setMinimumSize(QtCore.QSize(0, 40))
        self.exit_button.setFont(font)
        self.exit_button.setText('Exit')
        self.main_menu_buttons.addWidget(self.exit_button)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_menu_widget = MainMenuWidget()
    main_menu_widget.show()
    sys.exit(app.exec_())