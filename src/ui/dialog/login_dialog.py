import os
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QHBoxLayout, QPushButton
)

from service.data_service import DataService
from model.user_info import UserInfo
from util.messages import show_warn, show_error
from util.constants import COLOR_ACCENT, ICON_ICO


class LoginDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.user_data: UserInfo | None = None

        self.setWindowTitle("Вход")
        self.setMinimumWidth(420)

        if os.path.exists(ICON_ICO):
            self.setWindowIcon(QIcon(ICON_ICO))

        root = QVBoxLayout(self)
        form = QFormLayout()

        self.login_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        form.addRow("Логин:", self.login_edit)
        form.addRow("Пароль:", self.password_edit)

        root.addLayout(form)

        btns = QHBoxLayout()

        self.btn_login = QPushButton("Войти")
        self.btn_guest = QPushButton("Гость")

        self.btn_login.setStyleSheet(f"background:{COLOR_ACCENT}")
        self.btn_guest.setStyleSheet(f"background:{COLOR_ACCENT}")

        self.btn_login.clicked.connect(self.login)
        self.btn_guest.clicked.connect(self.guest)

        btns.addWidget(self.btn_login)
        btns.addWidget(self.btn_guest)

        root.addLayout(btns)

    def login(self):
        login = self.login_edit.text().strip()
        password = self.password_edit.text().strip()

        if not login or not password:
            show_warn(self, "Введите логин и пароль")
            return

        user = DataService.auth(login, password)

        if not user:
            show_error(self, "Неверный логин или пароль")
            return

        self.user_data = user
        self.accept()

    def guest(self):
        self.user_data = UserInfo(None, "Гость", "Гость")
        self.accept()