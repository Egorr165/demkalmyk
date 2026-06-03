from PyQt6.QtWidgets import QMessageBox


def show_error(parent, text):
    QMessageBox.critical(parent, "Ошибка", text)


def show_warn(parent, text):
    QMessageBox.warning(parent, "Предупреждение", text)