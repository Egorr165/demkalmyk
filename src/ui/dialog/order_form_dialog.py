"""
Форма добавления/редактирования заказа.
Поля по ТЗ: номер заказа, артикул, статус, пункт выдачи, даты.
Артикул задаётся строкой вида "PMEZMH, 2, BPV4MM, 2".
"""
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QHBoxLayout,
    QPushButton, QComboBox, QDateEdit, QLineEdit,
)
from service.data_service import DataService
from util.messages import show_error, show_warn


class OrderFormDialog(QDialog):
    def __init__(self, order_id=None):
        super().__init__()
        self.order_id = order_id

        self.setWindowTitle("Добавление/редактирование заказа")
        self.setMinimumWidth(700)

        root = QVBoxLayout(self)
        form = QFormLayout()

        self.order_number = QLineEdit()
        self.order_number.setReadOnly(True)

        self.articles = QLineEdit()
        self.articles.setPlaceholderText("Например: PMEZMH, 2, BPV4MM, 2")

        self.address = QComboBox()
        self.status = QComboBox()

        self.order_date = QDateEdit()
        self.order_date.setCalendarPopup(True)
        self.order_date.setDisplayFormat("yyyy-MM-dd")

        self.ship_date = QDateEdit()
        self.ship_date.setCalendarPopup(True)
        self.ship_date.setDisplayFormat("yyyy-MM-dd")

        form.addRow("Номер заказа:", self.order_number)
        form.addRow("Артикул:", self.articles)
        form.addRow("Адрес пункта выдачи:", self.address)
        form.addRow("Статус заказа:", self.status)
        form.addRow("Дата заказа:", self.order_date)
        form.addRow("Дата выдачи:", self.ship_date)

        # Заполняем выпадающие списки из справочников
        for a in DataService.get_addresses():
            self.address.addItem(
                f"{a['city_name']}, {a['street_name']} {a['house_number']}",
                a["id"],
            )
        for s in DataService.get_order_statuses():
            self.status.addItem(s["status_name"], s["id"])

        if self.order_id:
            self.load_order()
        else:
            self.order_number.setText(str(DataService.get_orders()[-1]["id"] + 1) if DataService.get_orders() else "1")
            self.generated_code = DataService.get_next_code()
            today = QDate.currentDate()
            self.order_date.setDate(today)
            self.ship_date.setDate(today.addDays(1))

        buttons = QHBoxLayout()
        save = QPushButton("Сохранить")
        back = QPushButton("Назад")
        save.clicked.connect(self.save_click)
        back.clicked.connect(self.reject)
        buttons.addWidget(save)
        buttons.addWidget(back)
        root.addLayout(buttons)

    def load_order(self):
        """Подгружаем данные существующего заказа в форму."""
        row = DataService.get_order_by_id(self.order_id)
        if not row:
            show_error(self, "Заказ не найден.")
            self.reject()
            return

        self.order_number.setText(str(row["id"]))
        # Собираем текст артикулов из order_items
        items = DataService.get_order_items(self.order_id)
        parts = [f"{it['article']}, {it['quantity']}" for it in items]
        self.articles.setText(", ".join(parts))

        self.generated_code = row["code"]

        idx = self.address.findData(row["address_id"])
        if idx >= 0:
            self.address.setCurrentIndex(idx)
        idx = self.status.findData(row["status_id"])
        if idx >= 0:
            self.status.setCurrentIndex(idx)

        if row["order_date"]:
            dt = row["order_date"]
            self.order_date.setDate(QDate(dt.year, dt.month, dt.day))
        if row["ship_date"]:
            dt = row["ship_date"]
            self.ship_date.setDate(QDate(dt.year, dt.month, dt.day))

    def save_click(self):
        articles = self.articles.text().strip()
        if not articles:
            show_warn(self, "Поле Артикул обязательно.")
            return
        try:
            DataService.parse_article_pairs(articles)
        except Exception as ex:
            show_error(self, str(ex))
            return

        model = {
            "id": self.order_id,
            "address_id": self.address.currentData(),
            "status_id": self.status.currentData(),
            "code": self.generated_code if not self.order_id else None,
            "order_date": self.order_date.date().toString("yyyy-MM-dd"),
            "ship_date": self.ship_date.date().toString("yyyy-MM-dd"),
            "article_text": articles,
        }
        try:
            DataService.save_order(model)
        except Exception as ex:
            show_error(self, f"Ошибка сохранения:\n{ex}")
            return
        self.accept()