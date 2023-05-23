from PyQt5.QtWidgets import QApplication, QMainWindow

from game.controllers.main_controller import MainController

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setFixedSize(800, 500)
    _ = MainController(main_window)
    main_window.show()
    sys.exit(app.exec_())
