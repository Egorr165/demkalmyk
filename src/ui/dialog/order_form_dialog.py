from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QPushButton,
    QComboBox,
    QDateEdit,
    QTableWidget,
    QSpinBox,
    QWidget,
)

from service.data_service import DataService
from util.messages import show_error


class OrderFormDialog(QDialog):

    def __init__(self, order_id=None):
        super().__init__()

        self.order_id = order_id

        self.setWindowTitle("Заказ")
        self.setMinimumWidth(800)

        root = QVBoxLayout(self)

        form = QFormLayout()
        root.addLayout(form)

        self.address_combo = QComboBox()
        self.status_combo = QComboBox()

        self.order_date_edit = QDateEdit()
        self.order_date_edit.setCalendarPopup(True)
        self.order_date_edit.setDisplayFormat("yyyy-MM-dd")

        self.ship_date_edit = QDateEdit()
        self.ship_date_edit.setCalendarPopup(True)
        self.ship_date_edit.setDisplayFormat("yyyy-MM-dd")

        form.addRow("Адрес:", self.address_combo)
        form.addRow("Статус:", self.status_combo)
        form.addRow("Дата заказа:", self.order_date_edit)
        form.addRow("Дата отгрузки:", self.ship_date_edit)

        for a in DataService.get_addresses():
            self.address_combo.addItem(
                f'{a["city_name"]}, {a["street_name"]} {a["house_number"]}',
                a["id"]
            )

        for s in DataService.get_order_statuses():
            self.status_combo.addItem(
                s["status_name"],
                s["id"]
            )

        self.items_table = QTableWidget()
        self.items_table.setColumnCount(2)
        self.items_table.setHorizontalHeaderLabels([
            "Товар",
            "Количество"
        ])

        root.addWidget(self.items_table)

        item_buttons = QHBoxLayout()

        add_item_btn = QPushButton("Добавить товар")
        remove_item_btn = QPushButton("Удалить товар")

        add_item_btn.clicked.connect(self.add_item_row)
        remove_item_btn.clicked.connect(self.remove_item_row)

        item_buttons.addWidget(add_item_btn)
        item_buttons.addWidget(remove_item_btn)
        item_buttons.addStretch()

        root.addLayout(item_buttons)

        if self.order_id:
            self.load_order()
        else:
            today = QDate.currentDate()

            self.order_date_edit.setDate(today)
            self.ship_date_edit.setDate(today)

            self.add_item_row()

        buttons = QHBoxLayout()

        save_btn = QPushButton("Сохранить")
        back_btn = QPushButton("Назад")

        save_btn.clicked.connect(self.save_click)
        back_btn.clicked.connect(self.reject)

        buttons.addWidget(save_btn)
        buttons.addWidget(back_btn)

        root.addLayout(buttons)

    def add_item_row(self, product_id=None, quantity=1):
        row = self.items_table.rowCount()
        self.items_table.insertRow(row)

        combo = QComboBox()

        for p in DataService.get_products():
            combo.addItem(
                f'{p["article"]} - {p["name"]}',
                p["id"]
            )

        if product_id is not None:
            index = combo.findData(product_id)
            if index >= 0:
                combo.setCurrentIndex(index)

        spin = QSpinBox()
        spin.setMinimum(1)
        spin.setMaximum(100000)
        spin.setValue(quantity)

        self.items_table.setCellWidget(row, 0, combo)
        self.items_table.setCellWidget(row, 1, spin)

    def remove_item_row(self):
        row = self.items_table.currentRow()

        if row >= 0:
            self.items_table.removeRow(row)

    def load_order(self):
        row = DataService.get_order_by_id(self.order_id)

        if not row:
            show_error(self, "Заказ не найден")
            self.reject()
            return

        index = self.address_combo.findData(row["address_id"])
        if index >= 0:
            self.address_combo.setCurrentIndex(index)

        index = self.status_combo.findData(row["status_id"])
        if index >= 0:
            self.status_combo.setCurrentIndex(index)

        if row["order_date"]:
            dt = row["order_date"]
            self.order_date_edit.setDate(
                QDate(dt.year, dt.month, dt.day)
            )

        if row["ship_date"]:
            dt = row["ship_date"]
            self.ship_date_edit.setDate(
                QDate(dt.year, dt.month, dt.day)
            )

        self.items_table.setRowCount(0)

        items = DataService.get_order_items(self.order_id)

        for item in items:
            self.add_item_row(
                item["product_id"],
                item["quantity"]
            )

    def save_click(self):
        if self.items_table.rowCount() == 0:
            show_error(self, "Добавьте хотя бы один товар")
            return

        items = []

        for row in range(self.items_table.rowCount()):
            combo = self.items_table.cellWidget(row, 0)
            spin = self.items_table.cellWidget(row, 1)

            items.append({
                "product_id": combo.currentData(),
                "quantity": spin.value(),
            })

        model = {
            "id": self.order_id,
            "address_id": self.address_combo.currentData(),
            "status_id": self.status_combo.currentData(),
            "code": DataService.get_next_code() if not self.order_id else None,
            "order_date": self.order_date_edit.date().toString("yyyy-MM-dd"),
            "ship_date": self.ship_date_edit.date().toString("yyyy-MM-dd"),
            "items": items,
        }

        try:
            DataService.save_order(model)
        except Exception as ex:
            show_error(self, str(ex))
            return

        self.accept()