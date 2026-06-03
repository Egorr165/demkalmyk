import os
from decimal import Decimal

from PyQt6.QtGui import QPixmap, QIcon, QColor, QFont
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QTableWidget,
    QTableWidgetItem, QListWidget, QListWidgetItem,
)
from service.data_service import DataService
from ui.dialog.login_dialog import LoginDialog
from ui.dialog.product_form_dialog import ProductFormDialog
from ui.dialog.orders_dialog import OrdersDialog
from util.constants import (
    ICON_PNG,
    ICON_ICO,
    PICTURE_PNG,
    COLOR_DISCOUNT_ROW,
    COLOR_ZERO_STOCK,
    COLOR_WHITE,
    COLOR_ACCENT,
    COLOR_SECOND, RESOURCES_DIR, PHOTOS_DIR, FONT,
)


class ProductsWindow(QMainWindow):

    def __init__(self, user):
        super().__init__()

        self.user = user
        self.goods = []

        self.setWindowTitle("Товары")
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
        header = QGridLayout()

        logo = QLabel()
        if os.path.exists(ICON_PNG):
            pix = QPixmap(ICON_PNG).scaled(120, 70)
            logo.setPixmap(pix)

        title = QLabel("Каталог товаров")
        title.setFont(QFont(FONT, 20))

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
        self.filters = QWidget()
        f = QHBoxLayout(self.filters)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск")

        self.supplier = QComboBox()
        self.sort = QComboBox()

        self.sort.addItems([
            "Без сортировки",
            "По количеству ↑",
            "По количеству ↓"
        ])

        f.addWidget(QLabel("Поиск"))
        f.addWidget(self.search)
        f.addWidget(QLabel("Поставщик"))
        f.addWidget(self.supplier)
        f.addWidget(QLabel("Сортировка"))
        f.addWidget(self.sort)

        layout.addWidget(self.filters)

        self.search.textChanged.connect(self.apply_filters)
        self.supplier.currentTextChanged.connect(self.apply_filters)
        self.sort.currentTextChanged.connect(self.apply_filters)

    def build_admin_panel(self, layout):
        self.admin_panel = QWidget()
        a = QHBoxLayout(self.admin_panel)

        self.btn_add = QPushButton("Добавить")
        self.btn_edit = QPushButton("Редактировать")
        self.btn_delete = QPushButton("Удалить")

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
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

    def load_data(self):
        self.goods = DataService.get_products()

        self.supplier.clear()
        self.supplier.addItem("Все")

        for g in self.goods:
            if g["supplier_name"] not in [self.supplier.itemText(i) for i in range(self.supplier.count())]:
                self.supplier.addItem(g["supplier_name"])

        self.apply_filters()

    def apply_filters(self):
        data = self.goods

        text = self.search.text().lower()
        supplier = self.supplier.currentText()
        sort = self.sort.currentText()

        if supplier != "Все":
            data = [x for x in data if x["supplier_name"] == supplier]

        if text:
            data = [
                x for x in data
                if text in (x["name"] or "").lower()
                   or text in (x["article"] or "").lower()
            ]

        if sort == "По количеству ↑":
            data.sort(key=lambda x: x["amount"])
        elif sort == "По количеству ↓":
            data.sort(key=lambda x: x["amount"], reverse=True)

        self.fill_table(data)

    def fill_table(self, rows):
        self.list_widget.clear()

        for r in rows:
            item_widget = QWidget()

            root = QHBoxLayout(item_widget)
            root.setContentsMargins(10, 10, 10, 10)

            # Фото
            photo_label = QLabel()

            path = (
                os.path.join(PHOTOS_DIR, os.path.basename(r["photo"]))
                if r["photo"]
                else PICTURE_PNG
            )

            pix = QPixmap(path)

            if pix.isNull():
                pix = QPixmap(PICTURE_PNG)

            photo_label.setPixmap(
                pix.scaled(
                    200,
                    200,
                    Qt.AspectRatioMode.KeepAspectRatio,
                )
            )

            root.addWidget(photo_label)

            # Информация
            info = QVBoxLayout()

            article = QLabel(
                f'{r["article"]} | {r["name"]}'
            )

            manufacturer = QLabel(
                f'Производитель: {r["manufacture_name"]}'
            )

            supplier = QLabel(
                f'Поставщик: {r["supplier_name"]}'
            )

            category = QLabel(
                f'Категория: {r["category_name"]}'
            )

            stock = QLabel(
                f'Остаток: {r["amount"]} {r["measure"]}'
            )

            info.addWidget(article)
            info.addWidget(manufacturer)
            info.addWidget(supplier)
            info.addWidget(category)
            info.addWidget(stock)

            root.addLayout(info)
            root.addStretch()

            # Блок скидки справа
            price = Decimal(str(r["cost"]))
            discount = Decimal(str(r["discount"]))
            final = price * (Decimal(100) - discount) / Decimal(100)

            discount_block = QVBoxLayout()

            old_price = QLabel(f"{price:.2f} ₽")

            if discount > 0:
                f = old_price.font()
                f.setStrikeOut(True)
                old_price.setFont(f)
                old_price.setStyleSheet("color:red;")

            final_price = QLabel(f"{final:.2f} ₽")
            final_price.setFont(QFont(FONT, 12, QFont.Weight.Bold))

            discount_label = QLabel(
                f"Скидка {discount}%"
            )

            discount_block.addWidget(old_price)
            discount_block.addWidget(final_price)
            discount_block.addWidget(discount_label)

            root.addLayout(discount_block)

            if r["amount"] == 0:
                item_widget.setStyleSheet(
                    f"background:{COLOR_ZERO_STOCK};"
                )
            elif discount > 15:
                item_widget.setStyleSheet(
                    f"background:{COLOR_DISCOUNT_ROW};"
                )

            item = QListWidgetItem()

            item.setData(
                Qt.ItemDataRole.UserRole,
                r["id"]
            )

            item.setSizeHint(
                item_widget.sizeHint()
            )

            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(
                item,
                item_widget
            )

    def selected_id(self):
        item = self.list_widget.currentItem()

        if not item:
            return None

        return item.data(Qt.ItemDataRole.UserRole)

    def add_good(self):
        dlg = ProductFormDialog(None)
        if dlg.exec():
            self.load_data()

    def edit_good(self):
        gid = self.selected_id()
        if not gid:
            return
        dlg = ProductFormDialog(gid)
        if dlg.exec():
            self.load_data()

    def delete_good(self):
        gid = self.selected_id()
        if not gid:
            return

        DataService.delete_product(gid)
        self.load_data()

    def apply_role_rules(self):
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
