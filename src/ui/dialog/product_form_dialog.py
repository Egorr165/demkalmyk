import os
import uuid
import shutil

from decimal import Decimal

from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QGridLayout, QLabel,
    QLineEdit, QTextEdit, QComboBox,
    QPushButton, QHBoxLayout, QFileDialog, QFormLayout
)

from service.data_service import DataService
from util.constants import PHOTOS_DIR, PICTURE_PNG, ICON_ICO
from util.messages import show_error, show_warn

class ProductFormDialog(QDialog):

    def __init__(self, good_id=None):
        super().__init__()

        self.good_id = good_id
        self.old_photo = ""
        self.new_photo_path = ""

        self.setWindowTitle("Товар")
        self.setMinimumWidth(1000)

        if os.path.exists(ICON_ICO):
            self.setWindowIcon(QIcon(ICON_ICO))

        root = QVBoxLayout(self)

        content = QHBoxLayout()
        root.addLayout(content)

        # Фото

        photo_block = QVBoxLayout()

        self.photo = QLabel()
        self.photo.setFixedSize(300, 200)
        self.photo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_photo = QPushButton("Выбрать фото")
        btn_photo.clicked.connect(self.select_photo)

        photo_block.addWidget(self.photo)
        photo_block.addWidget(btn_photo)
        photo_block.addStretch()

        # Информация

        form = QFormLayout()

        self.id_edit = QLineEdit()
        self.id_edit.setReadOnly(True)

        self.article = QLineEdit()
        self.name = QLineEdit()
        self.category = QComboBox()
        self.description = QTextEdit()
        self.manufacture = QComboBox()
        self.supplier = QLineEdit()
        self.cost = QLineEdit()
        self.measure = QLineEdit()
        self.amount = QLineEdit()

        form.addRow("ID", self.id_edit)
        form.addRow("Артикул", self.article)
        form.addRow("Название", self.name)
        form.addRow("Категория", self.category)
        form.addRow("Описание", self.description)
        form.addRow("Производитель", self.manufacture)
        form.addRow("Поставщик", self.supplier)
        form.addRow("Цена", self.cost)
        form.addRow("Ед. измерения", self.measure)
        form.addRow("Количество", self.amount)

        # Скидка

        discount_block = QVBoxLayout()

        discount_title = QLabel("Скидка (%)")
        discount_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.discount = QLineEdit()

        discount_block.addWidget(discount_title)
        discount_block.addWidget(self.discount)
        discount_block.addStretch()

        # Сборка

        content.addLayout(photo_block, 2)
        content.addLayout(form, 4)
        content.addLayout(discount_block, 1)

        # Кнопки

        btns = QHBoxLayout()

        save = QPushButton("Сохранить")
        back = QPushButton("Назад")

        save.clicked.connect(self.save)
        back.clicked.connect(self.reject)

        btns.addWidget(save)
        btns.addWidget(back)

        root.addLayout(btns)

        self.load_refs()

        if self.good_id:
            self.load()
        else:
            self.photo.setPixmap(
                QPixmap(PICTURE_PNG).scaled(
                    300,
                    200,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )

    def load_refs(self):
        for c in DataService.get_categories():
            self.category.addItem(c["category_name"], c["id"])

        for m in DataService.get_manufactures():
            self.manufacture.addItem(m["manufacture_name"], m["id"])

    def load(self):
        row = DataService.get_product_by_id(self.good_id)

        self.id_edit.setText(str(row["id"]))
        self.article.setText(row["article"])
        self.name.setText(row["name"])
        self.description.setPlainText(row["description"])
        self.supplier.setText(row["supplier_name"])
        self.cost.setText(str(row["cost"]))
        self.measure.setText(row["measure"])
        self.amount.setText(str(row["amount"]))
        self.discount.setText(str(row["discount"]))

        self.old_photo = row["photo"] or ""

        if self.old_photo:
            path = os.path.join(
                "import/photos",
                os.path.basename(self.old_photo)
            )

            pix = QPixmap(path)

            if not pix.isNull():
                self.photo.setPixmap(
                    pix.scaled(
                        300,
                        200,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                )

        i = self.category.findData(row["category_id"])
        if i >= 0:
            self.category.setCurrentIndex(i)

        j = self.manufacture.findData(row["manufacture_id"])
        if j >= 0:
            self.manufacture.setCurrentIndex(j)

    def select_photo(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите фото",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if path:
            self.new_photo_path = path

            self.photo.setPixmap(
                QPixmap(path).scaled(
                    300,
                    200,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )

    def save(self):
        try:
            model = {
                "id": self.good_id,
                "article": self.article.text(),
                "name": self.name.text(),
                "category_id": self.category.currentData(),
                "description": self.description.toPlainText(),
                "manufacture_id": self.manufacture.currentData(),
                "supplier_name": self.supplier.text(),
                "cost": Decimal(self.cost.text()),
                "measure": self.measure.text(),
                "amount": int(self.amount.text()),
                "discount": Decimal(self.discount.text()),
                "photo": self.old_photo,
            }
        except Exception:
            show_error(self, "Ошибка данных")
            return

        if self.new_photo_path:
            os.makedirs(PHOTOS_DIR, exist_ok=True)

            name = f"{uuid.uuid4().hex}.png"
            path = os.path.join(PHOTOS_DIR, name)

            shutil.copy2(self.new_photo_path, path)

            model["photo"] = f"resources/photos/{name}"

        DataService.save_product(model)

        self.accept()