"""
Модуль работы с базой данных.
Инкапсулирует все SQL-запросы, чтобы UI-слой не зависел от структуры БД.
"""
from model.user_info import UserInfo
from db.connector import get_connection


class DataService:
    # Авторизация: проверяем логин и пароль в таблице users
    @staticmethod
    def auth(login: str, password: str):
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT u.id, u.full_name, r.role_name
                FROM users u
                JOIN roles r ON r.id = u.role_id
                WHERE u.login = %s AND u.password = %s
                """,
                (login, password),
            )
            row = cur.fetchone()
            if not row:
                return None
            return UserInfo(row["id"], row["full_name"], row["role_name"])
        finally:
            conn.close()

    # Список товаров с JOIN всех справочников
    @staticmethod
    def get_products():
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT
                    p.id, p.article, p.name, c.category_name,
                    p.description, m.manufacture_name, s.supplier_name,
                    p.cost, p.measure, p.amount, p.discount, p.photo
                FROM products p
                JOIN categories c ON c.id = p.category_id
                JOIN manufacturers m ON m.id = p.manufacture_id
                JOIN suppliers s ON s.id = p.supplier_id
                ORDER BY p.id
                """
            )
            return cur.fetchall()
        finally:
            conn.close()

    # Список поставщиков для выпадающего списка (если понадобится)
    @staticmethod
    def get_supplier_names():
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT supplier_name FROM suppliers ORDER BY supplier_name")
            return [x[0] for x in cur.fetchall()]
        finally:
            conn.close()

    # Список производителей для фильтра по ТЗ Варианта 3
    @staticmethod
    def get_manufacture_names():
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT manufacture_name FROM manufacturers ORDER BY manufacture_name")
            return [x[0] for x in cur.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def get_categories():
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT id, category_name FROM categories ORDER BY category_name")
            return cur.fetchall()
        finally:
            conn.close()

    # Выпадающий список производителей в форме товара
    @staticmethod
    def get_manufactures():
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                "SELECT id, manufacture_name FROM manufacturers ORDER BY manufacture_name"
            )
            return cur.fetchall()
        finally:
            conn.close()

    # Карточка товара для формы редактирования
    @staticmethod
    def get_product_by_id(product_id: int):
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT p.id, p.article, p.name, p.category_id, p.description,
                       p.manufacture_id, p.supplier_id, s.supplier_name,
                       p.cost, p.measure, p.amount, p.discount, p.photo
                FROM products p
                JOIN suppliers s ON s.id = p.supplier_id
                WHERE p.id = %s
                """,
                (product_id,),
            )
            return cur.fetchone()
        finally:
            conn.close()

    # Гарантирует, что поставщик есть в справочнике (создаёт при необходимости)
    @staticmethod
    def ensure_supplier(conn, supplier_name: str):
        cur = conn.cursor()
        cur.execute("SELECT id FROM suppliers WHERE supplier_name = %s", (supplier_name,))
        row = cur.fetchone()
        if row:
            return row[0]
        cur.execute("INSERT INTO suppliers(supplier_name) VALUES(%s)", (supplier_name,))
        conn.commit()
        return cur.lastrowid

    # Добавление/обновление товара
    @staticmethod
    def save_product(model: dict):
        conn = get_connection()
        try:
            supplier_id = DataService.ensure_supplier(conn, model["supplier_name"])
            cur = conn.cursor()
            if model.get("id"):
                cur.execute(
                    """
                    UPDATE products
                    SET article=%s, name=%s, measure=%s, cost=%s,
                        supplier_id=%s, manufacture_id=%s, category_id=%s,
                        discount=%s, amount=%s, description=%s, photo=%s
                    WHERE id=%s
                    """,
                    (
                        model["article"], model["name"], model["measure"],
                        model["cost"], supplier_id, model["manufacture_id"],
                        model["category_id"], model["discount"],
                        model["amount"], model["description"],
                        model["photo"], model["id"],
                    ),
                )
            else:
                cur.execute(
                    """
                    INSERT INTO products(
                        article, name, measure, cost, supplier_id,
                        manufacture_id, category_id, discount, amount,
                        description, photo
                    ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """,
                    (
                        model["article"], model["name"], model["measure"],
                        model["cost"], supplier_id, model["manufacture_id"],
                        model["category_id"], model["discount"],
                        model["amount"], model["description"],
                        model["photo"],
                    ),
                )
            conn.commit()
        finally:
            conn.close()

    # Проверка: есть ли товар в заказах (чтобы запретить удаление)
    @staticmethod
    def product_in_orders(product_id: int) -> bool:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM order_items WHERE product_id = %s", (product_id,))
            return cur.fetchone()[0] > 0
        finally:
            conn.close()

    @staticmethod
    def delete_product(product_id: int):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def get_order_items(order_id: int):
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT oi.id, oi.product_id, oi.quantity,
                       p.article, p.name, p.cost
                FROM order_items oi
                JOIN products p ON p.id = oi.product_id
                WHERE oi.order_id = %s
                ORDER BY p.name
                """,
                (order_id,),
            )
            return cur.fetchall()
        finally:
            conn.close()

    # Список заказов со склейкой адреса в одну строку (по ТЗ)
    @staticmethod
    def get_orders():
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT
                    o.id, o.code, o.order_date, o.ship_date,
                    s.status_name,
                    CONCAT(a.city_name, ', ', a.street_name, ' ', a.house_number) AS address_text
                FROM orders o
                JOIN order_statuses s ON s.id = o.status_id
                JOIN addresses a ON a.id = o.address_id
                ORDER BY o.id
                """
            )
            return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_order_by_id(order_id: int):
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
            return cur.fetchone()
        finally:
            conn.close()

    @staticmethod
    def get_order_statuses():
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT id, status_name FROM order_statuses ORDER BY status_name")
            return cur.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_addresses():
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT id, address_index, city_name, street_name, house_number
                FROM addresses ORDER BY id
                """
            )
            return cur.fetchall()
        finally:
            conn.close()

    # Генерация следующего кода получения заказа
    @staticmethod
    def get_next_code():
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT COALESCE(MAX(code), 900) + 1 FROM orders")
            return cur.fetchone()[0]
        finally:
            conn.close()

    # Парсинг строки артикулов вида "PMEZMH, 2, BPV4MM, 2"
    @staticmethod
    def parse_article_pairs(text: str):
        tokens = [x.strip() for x in (text or "").split(",") if x.strip()]
        if len(tokens) < 2 or len(tokens) % 2 != 0:
            raise ValueError("Артикулы задаются парами: артикул, количество.")
        pairs = []
        for i in range(0, len(tokens), 2):
            article = tokens[i]
            try:
                qty = int(tokens[i + 1])
            except Exception:
                raise ValueError("Количество должно быть целым числом.")
            if qty <= 0:
                raise ValueError("Количество должно быть больше 0.")
            pairs.append((article, qty))
        return pairs

    # Сохранение заказа: принимает article_text строкой
    @staticmethod
    def save_order(model: dict):
        conn = get_connection()
        try:
            pairs = DataService.parse_article_pairs(model["article_text"])
            cur = conn.cursor()

            # Находим product_id для каждого артикула
            article_ids = {}
            for article, _ in pairs:
                cur.execute("SELECT id FROM products WHERE article = %s", (article,))
                row = cur.fetchone()
                if not row:
                    raise ValueError(f"Артикул {article} не найден в таблице products.")
                article_ids[article] = row[0]

            if model.get("id"):
                cur.execute(
                    """
                    UPDATE orders
                    SET address_id=%s, status_id=%s, order_date=%s, ship_date=%s
                    WHERE id = %s
                    """,
                    (
                        model["address_id"], model["status_id"],
                        model["order_date"], model["ship_date"], model["id"],
                    ),
                )
                order_id = model["id"]
                cur.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))
            else:
                cur.execute(
                    """
                    INSERT INTO orders(address_id, user_id, code, status_id, order_date, ship_date)
                    VALUES(%s, NULL, %s, %s, %s, %s)
                    """,
                    (
                        model["address_id"], model["code"], model["status_id"],
                        model["order_date"], model["ship_date"],
                    ),
                )
                order_id = cur.lastrowid

            # Заполняем позиции заказа
            for article, qty in pairs:
                cur.execute(
                    "INSERT INTO order_items(order_id, product_id, quantity) VALUES(%s,%s,%s)",
                    (order_id, article_ids[article], qty),
                )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def delete_order(order_id: int):
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM orders WHERE id = %s", (order_id,))
            conn.commit()
        finally:
            conn.close()