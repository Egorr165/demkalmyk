"""
Главное окно приложения — список товаров.
Отображает данные из БД с учётом роли пользователя.
"""
import os
from decimal import Decimal
from PyQt6.QtGui import QPixmap, QIcon, QColor, QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QLineEdit, QComboBox,
    QTableWidget, QTableWidgetItem,
)
from service.data_service import DataService
from ui.dialog.login_dialog import LoginDialog
from ui.dialog.product_form_dialog import ProductFormDialog
from ui.dialog.orders_dialog import OrdersDialog
from util.constants import (
    ICON_PNG, ICON_ICO, PICTURE_PNG,
    COLOR_DISCOUNT_ROW, COLOR_ZERO_STOCK, COLOR_WHITE,
    COLOR_ACCENT, COLOR_SECOND, PHOTOS_DIR, FONT,
)


class ProductsWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.goods = []
        self.editor_opened = False  # флаг для блокировки второго окна редактирования

        self.setWindowTitle("ООО «СтройМатериалы» — Список товаров")
        self.resize(1500, 800)
        if os.path.exists(ICON_ICO):
            self.setWindowIcon(QIcon(ICON_ICO))

        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)

        self.build_header(layout)
        self.build_filters(layout)
        self.build_admin_panel(layout)
        self.build_table(layout)

        self.apply_role_rules()
        self.load_data()

    def build_header(self, layout):
        """Шапка: логотип, заголовок, роль, ФИО, кнопки."""
        header = QGridLayout()

        logo = QLabel()
        if os.path.exists(ICON_PNG):
            pix = QPixmap(ICON_PNG).scaled(120, 70, Qt.AspectRatioMode.KeepAspectRatio)
            logo.setPixmap(pix)

        title = QLabel("ООО «СтройМатериалы»")
        title.setFont(QFont(FONT, 20, QFont.Weight.Bold))

        self.role_label = QLabel(f"Роль: {self.user.role_name}")
        self.user_label = QLabel(f"{self.user.full_name}")

        self.btn_orders = QPushButton("Заказы")
        self.btn_logout = QPushButton("Выход")

        self.btn_orders.clicked.connect(self.open_orders)
        self.btn_logout.clicked.connect(self.logout)

        right = QVBoxLayout()
        right.addWidget(self.role_label, alignment=Qt.AlignmentFlag.AlignRight)
        right.addWidget(self.user_label, alignment=Qt.AlignmentFlag.AlignRight)
        right.addWidget(self.btn_orders, alignment=Qt.AlignmentFlag.AlignRight)
        right.addWidget(self.btn_logout, alignment=Qt.AlignmentFlag.AlignRight)

        header.addWidget(logo, 0, 0)
        header.addWidget(title, 0, 1)
        header.addLayout(right, 0, 2)
        header.setColumnStretch(1, 1)

        layout.addLayout(header)

    def build_filters(self, layout):
        """Панель фильтров/поиска/сортировки — только для менеджера и админа."""
        self.filters = QWidget()
        f = QHBoxLayout(self.filters)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск по всем полям...")

        # ТЗ: фильтр по ПРОИЗВОДИТЕЛЮ (не по поставщику)
        self.manufacture = QComboBox()

        # ТЗ: сортировка по остатку, цене и скидке
        self.sort = QComboBox()
        self.sort.addItems([
            "Без сортировки",
            "По количеству ↑", "По количеству ↓",
            "По цене ↑", "По цене ↓",
            "По скидке ↑", "По скидке ↓",
        ])

        f.addWidget(QLabel("Поиск:"))
        f.addWidget(self.search, 2)
        f.addWidget(QLabel("Производитель:"))
        f.addWidget(self.manufacture, 1)
        f.addWidget(QLabel("Сортировка:"))
        f.addWidget(self.sort, 1)

        layout.addWidget(self.filters)

        # Реакция на изменение в реальном времени (без кнопки «Найти»)
        self.search.textChanged.connect(self.apply_filters)
        self.manufacture.currentTextChanged.connect(self.apply_filters)
        self.sort.currentTextChanged.connect(self.apply_filters)

    def build_admin_panel(self, layout):
        """Панель CRUD-кнопок — только для администратора."""
        self.admin_panel = QWidget()
        a = QHBoxLayout(self.admin_panel)

        self.btn_add = QPushButton("Добавить товар")
        self.btn_edit = QPushButton("Редактировать товар")
        self.btn_delete = QPushButton("Удалить товар")

        self.btn_add.clicked.connect(self.add_good)
        self.btn_edit.clicked.connect(self.edit_good)
        self.btn_delete.clicked.connect(self.delete_good)

        self.btn_add.setStyleSheet(f"background:{COLOR_ACCENT}")
        self.btn_edit.setStyleSheet(f"background:{COLOR_SECOND}")
        self.btn_delete.setStyleSheet(f"background:{COLOR_SECOND}")

        a.addWidget(self.btn_add)
        a.addWidget(self.btn_edit)
        a.addWidget(self.btn_delete)
        a.addStretch()

        layout.addWidget(self.admin_panel)

    def build_table(self, layout):
        """Таблица товаров — 12 колонок по макету ТЗ."""
        self.table = QTableWidget()
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels([
            "Фото", "Артикул", "Наименование", "Категория", "Описание",
            "Производитель", "Поставщик", "Цена", "Цена со скидкой",
            "Ед.", "Остаток", "Скидка",
        ])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self.row_double_click)
        layout.addWidget(self.table)

    def load_data(self):
        self.goods = DataService.get_products()

        # Заполняем выпадающий список производителей
        self.manufacture.clear()
        self.manufacture.addItem("Все производители")
        for m in DataService.get_manufacture_names():
            self.manufacture.addItem(m)

        self.apply_filters()

    def apply_filters(self):
        """Совместное применение поиска + фильтра + сортировки."""
        data = list(self.goods)

        # Фильтрация и поиск доступны только менеджеру и администратору
        if self.user.role_name in ("Администратор", "Менеджер"):
            text = self.search.text().lower()
            manufacture = self.manufacture.currentText()
            sort_mode = self.sort.currentText()

            # Фильтр по производителю
            if manufacture != "Все производители":
                data = [x for x in data if x["manufacture_name"] == manufacture]

            # Поиск по всем текстовым полям
            if text:
                def hit(row):
                    fields = [
                        row.get("article"), row.get("name"),
                        row.get("category_name"), row.get("description"),
                        row.get("manufacture_name"), row.get("supplier_name"),
                        row.get("measure"),
                    ]
                    return any(text in str(v or "").lower() for v in fields)
                data = [x for x in data if hit(x)]

            # Сортировка (6 режимов по ТЗ)
            if sort_mode == "По количеству ↑":
                data.sort(key=lambda x: x["amount"])
            elif sort_mode == "По количеству ↓":
                data.sort(key=lambda x: x["amount"], reverse=True)
            elif sort_mode == "По цене ↑":
                data.sort(key=lambda x: x["cost"])
            elif sort_mode == "По цене ↓":
                data.sort(key=lambda x: x["cost"], reverse=True)
            elif sort_mode == "По скидке ↑":
                data.sort(key=lambda x: x["discount"])
            elif sort_mode == "По скидке ↓":
                data.sort(key=lambda x: x["discount"], reverse=True)

        self.fill_table(data)

    def fill_table(self, rows):
        """Заполнение таблицы с подсветкой строк по ТЗ."""
        self.table.setRowCount(len(rows))
        for i, r in enumerate(rows):
            # Фото товара (или заглушка)
            photo_label = QLabel()
            path = os.path.join(PHOTOS_DIR, r["photo"]) if r["photo"] else PICTURE_PNG
            if not os.path.exists(path):
                path = PICTURE_PNG
            pix = QPixmap(path).scaled(80, 60, Qt.AspectRatioMode.KeepAspectRatio)
            photo_label.setPixmap(pix)
            photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setCellWidget(i, 0, photo_label)

            # Расчёт цены со скидкой
            price = Decimal(str(r["cost"]))
            discount = Decimal(str(r["discount"]))
            final = price * (Decimal(100) - discount) / Decimal(100)

            values = [
                r["article"], r["name"], r["category_name"], r["description"],
                r["manufacture_name"], r["supplier_name"],
                f"{price:.2f}", f"{final:.2f}",
                r["measure"], str(r["amount"]), f"{discount:.2f}",
            ]
            for c, v in enumerate(values, start=1):
                item = QTableWidgetItem(str(v))
                item.setData(Qt.ItemDataRole.UserRole, r["id"])
                self.table.setItem(i, c, item)

            # Зачёркивание старой цены красным, если есть скидка
            if discount > 0:
                price_item = self.table.item(i, 7)
                f = price_item.font()
                f.setStrikeOut(True)
                price_item.setFont(f)
                price_item.setForeground(QColor("red"))

            # Подсветка строк по ТЗ:
            # - остаток = 0 → голубой
            # - скидка > 12% → #F4A460
            bg_color = QColor(COLOR_WHITE)
            if r["amount"] == 0:
                bg_color = QColor(COLOR_ZERO_STOCK)
            elif discount > 12:
                bg_color = QColor(COLOR_DISCOUNT_ROW)

            for c in range(1, self.table.columnCount()):
                cell = self.table.item(i, c)
                if cell:
                    cell.setBackground(bg_color)

        self.table.resizeColumnsToContents()
        self.table.setColumnWidth(0, 90)

    def selected_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 1)
        return item.data(Qt.ItemDataRole.UserRole) if item else None

    def row_double_click(self):
        """Двойной клик — переход к редактированию (только админ)."""
        if self.user.role_name == "Администратор":
            self.edit_good()

    def add_good(self):
        if self.editor_opened:
            return
        self.editor_opened = True
        dlg = ProductFormDialog(None)
        if dlg.exec():
            self.load_data()
        self.editor_opened = False

    def edit_good(self):
        gid = self.selected_id()
        if not gid:
            return
        if self.editor_opened:
            return
        self.editor_opened = True
        dlg = ProductFormDialog(gid)
        if dlg.exec():
            self.load_data()
        self.editor_opened = False

    def delete_good(self):
        """Удаление товара: запрещено, если товар есть в заказах."""
        gid = self.selected_id()
        if not gid:
            return
        if DataService.product_in_orders(gid):
            from util.messages import show_warn
            show_warn(self, "Товар присутствует в заказе. Удаление невозможно.")
            return
        from util.messages import show_error
        try:
            DataService.delete_product(gid)
        except Exception as ex:
            show_error(self, f"Ошибка удаления:\n{ex}")
            return
        self.load_data()

    def apply_role_rules(self):
        """Скрытие/показ элементов интерфейса в зависимости от роли."""
        is_admin = self.user.role_name == "Администратор"
        is_manager = self.user.role_name in ("Администратор", "Менеджер")

        self.admin_panel.setVisible(is_admin)
        self.btn_orders.setVisible(is_manager)
        self.filters.setVisible(is_manager)

    def open_orders(self):
        dlg = OrdersDialog(self.user)
        dlg.exec()

    def logout(self):
        self.close()
        login = LoginDialog()
        if login.exec():
            self.next = ProductsWindow(login.user_data)
            self.next.show()