from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from game.views.widgets.my_button import MyButton
from game.views.widgets.my_label import MyLabel
from game.views.widgets.settings_layuot import SettingsWidget


class SaveExitButtonsWidget(QWidget):
    def __init__(self, widget: QWidget = None):
        super().__init__(widget)
        self.setFixedSize(391, 71)

        self.layout = QHBoxLayout(self)
        self.save_and_exit_button = MyButton(40, 15, 'Save and exit', self)
        self.exit_button = MyButton(40, 15, 'Exit', self)

        self.setup_layout()

    def setup_layout(self):
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.save_and_exit_button)
        self.layout.addWidget(self.exit_button)


class SettingsMenuView(QWidget):
    def __init__(self, widget: QWidget = None):
        super().__init__(widget)
        self.setFixedSize(800, 500)
        self.title = MyLabel(25, 'Settings', self)
        self.title.setGeometry(QtCore.QRect(0, 0, 800, 60))

        self.settings = SettingsWidget(self)
        self.settings.move(270, 80)
        self.save_exit_buttons = SaveExitButtonsWidget(self)
        self.save_exit_buttons.move(210, 410)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = SettingsMenuView()
    # ui = Ui_Form()
    # ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())