from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox, QListWidget, QListWidgetItem, QWidget,
)
from PyQt6.QtCore import Qt

from service.data_service import DataService
from ui.dialog.order_form_dialog import OrderFormDialog
from util.messages import show_warn, show_error

class OrdersDialog(QDialog):

    def __init__(self, user):
        super().__init__()

        self.user = user

        self.setWindowTitle("Заказы")
        self.resize(1200, 650)

        root = QVBoxLayout(self)

        top = QHBoxLayout()

        title = QLabel("Список заказов")
        top.addWidget(title)
        top.addStretch()

        self.btn_add = QPushButton("Добавить")
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

        # список вместо таблицы
        self.list_widget = QListWidget()
        self.list_widget.itemDoubleClicked.connect(self.double_click_order)
        root.addWidget(self.list_widget)

        is_admin = self.user.role_name == "Администратор"

        self.btn_add.setVisible(is_admin)
        self.btn_edit.setVisible(is_admin)
        self.btn_delete.setVisible(is_admin)

        self.load_orders()

    def load_orders(self):
        self.list_widget.clear()

        rows = DataService.get_orders()

        for row in rows:
            item_widget = QWidget()
            root = QHBoxLayout(item_widget)
            root.setContentsMargins(10, 10, 10, 10)

            # LEFT
            left = QVBoxLayout()

            id_lbl = QLabel(f"Заказ №{row['id']}")
            code_lbl = QLabel(f"Код: {row['code']}")
            status_lbl = QLabel(f"Статус: {row['status_name']}")

            address = (
                f"{row['city_name']}, "
                f"{row['street_name']} "
                f"{row['house_number']}"
            )

            address_lbl = QLabel(f"Адрес: {address}")
            order_date_lbl = QLabel(f"Дата заказа: {row['order_date']}")

            left.addWidget(id_lbl)
            left.addWidget(code_lbl)
            left.addWidget(status_lbl)
            left.addWidget(address_lbl)
            left.addWidget(order_date_lbl)

            # RIGHT
            right = QVBoxLayout()

            ship_lbl = QLabel("Дата доставки")
            ship_lbl.setStyleSheet("font-weight: bold;")

            ship_date = QLabel(str(row['ship_date']))

            right.addStretch()
            right.addWidget(ship_lbl)
            right.addWidget(ship_date)
            right.addStretch()

            root.addLayout(left)
            root.addStretch()
            root.addLayout(right)

            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, row["id"])
            item.setSizeHint(item_widget.sizeHint())

            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, item_widget)

    def current_order_id(self):
        item = self.list_widget.currentItem()
        if not item:
            return None
        return item.data(Qt.ItemDataRole.UserRole)

    def add_order(self):
        dlg = OrderFormDialog()
        if dlg.exec():
            self.load_orders()

    def edit_order(self):
        order_id = self.current_order_id()

        if not order_id:
            show_warn(self, "Выберите заказ")
            return

        dlg = OrderFormDialog(order_id)
        if dlg.exec():
            self.load_orders()

    def double_click_order(self, _):
        if self.user.role_name == "Администратор":
            self.edit_order()

    def delete_order(self):
        order_id = self.current_order_id()

        if not order_id:
            show_warn(self, "Выберите заказ")
            return

        ans = QMessageBox.question(self, "Подтверждение", "Удалить заказ?")
        if ans != QMessageBox.StandardButton.Yes:
            return

        try:
            DataService.delete_order(order_id)
        except Exception as ex:
            show_error(self, str(ex))
            return

        self.load_orders()