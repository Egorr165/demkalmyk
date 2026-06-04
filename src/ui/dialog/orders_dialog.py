"""
Окно списка заказов. Таблица с 6 колонками по макету.
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QMessageBox,
)
from PyQt6.QtCore import Qt
from service.data_service import DataService
from ui.dialog.order_form_dialog import OrderFormDialog
from util.messages import show_warn, show_error


class OrdersDialog(QDialog):
    def __init__(self, user):
        super().__init__()
        self.user = user

        self.setWindowTitle("Список заказов")
        self.resize(1200, 650)

        root = QVBoxLayout(self)

        top = QHBoxLayout()
        title = QLabel("Список заказов")
        title.setStyleSheet("font-size:24px; font-weight:bold;")
        top.addWidget(title)
        top.addStretch()

        self.btn_add = QPushButton("Добавить заказ")
        self.btn_edit = QPushButton("Редактировать")
        self.btn_delete = QPushButton("Удалить")
        btn_close = QPushButton("Назад")

        self.btn_add.clicked.connect(self.add_order)
        self.btn_edit.clicked.connect(self.edit_order)
        self.btn_delete.clicked.connect(self.delete_order)
        btn_close.clicked.connect(self.close)

        top.addWidget(self.btn_add)
        top.addWidget(self.btn_edit)
        top.addWidget(self.btn_delete)
        top.addWidget(btn_close)
        root.addLayout(top)

        # Таблица вместо списка — строго по макету ТЗ
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Номер", "Артикул заказа", "Статус",
            "Пункт выдачи", "Дата заказа", "Дата выдачи",
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.doubleClicked.connect(self.double_click_order)
        root.addWidget(self.table)

        # CRUD-кнопки только у администратора
        is_admin = self.user.role_name == "Администратор"
        self.btn_add.setVisible(is_admin)
        self.btn_edit.setVisible(is_admin)
        self.btn_delete.setVisible(is_admin)

        self.load_orders()

    def load_orders(self):
        """Загружаем заказы из БД и заполняем таблицу."""
        self.table.setRowCount(0)
        rows = DataService.get_orders()
        for i, r in enumerate(rows):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QTableWidgetItem(str(r["id"])))
            self.table.setItem(i, 1, QTableWidgetItem(self.get_article_text(r["id"])))
            self.table.setItem(i, 2, QTableWidgetItem(r["status_name"]))
            self.table.setItem(i, 3, QTableWidgetItem(r["address_text"]))
            self.table.setItem(i, 4, QTableWidgetItem(str(r["order_date"])))
            self.table.setItem(i, 5, QTableWidgetItem(str(r["ship_date"])))
            self.table.item(i, 0).setData(Qt.ItemDataRole.UserRole, r["id"])
        self.table.resizeColumnsToContents()

    # Достаём текст артикулов заказа (склеиваем из order_items)
    @staticmethod
    def get_article_text(order_id: int) -> str:
        items = DataService.get_order_items(order_id)
        parts = [f"{it['article']}, {it['quantity']}" for it in items]
        return ", ".join(parts)

    def current_order_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 0)
        return item.data(Qt.ItemDataRole.UserRole) if item else None

    def double_click_order(self):
        if self.user.role_name == "Администратор":
            self.edit_order()

    def add_order(self):
        dlg = OrderFormDialog(None)
        if dlg.exec():
            self.load_orders()

    def edit_order(self):
        oid = self.current_order_id()
        if not oid:
            show_warn(self, "Выберите заказ для редактирования.")
            return
        dlg = OrderFormDialog(oid)
        if dlg.exec():
            self.load_orders()

    def delete_order(self):
        oid = self.current_order_id()
        if not oid:
            show_warn(self, "Выберите заказ для удаления.")
            return
        ans = QMessageBox.question(self, "Подтверждение", "Удалить выбранный заказ?")
        if ans != QMessageBox.StandardButton.Yes:
            return
        try:
            DataService.delete_order(oid)
        except Exception as ex:
            show_error(self, f"Ошибка удаления:\n{ex}")
            return
        self.load_orders()