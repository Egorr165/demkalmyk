import sys

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

from ui.dialog.login_dialog import LoginDialog
from ui.window.products_window import ProductsWindow
from util.constants import FONT


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setFont(QFont(FONT, 11, QFont.Weight.Bold))

    login = LoginDialog()

    if not login.exec():
        sys.exit(0)

    window = ProductsWindow(login.user_data)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()