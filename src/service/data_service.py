from model.user_info import UserInfo
from db.connector import get_connection


class DataService:

    @staticmethod
    def auth(login: str, password: str):
        conn = get_connection()

        try:
            cur = conn.cursor(dictionary=True)

            cur.execute(
                """
                SELECT
                    u.id,
                    u.full_name,
                    r.role_name
                FROM users u
                         JOIN roles r ON r.id = u.role_id
                WHERE u.login = %s
                  AND u.password = %s
                """,
                (login, password),
            )

            row = cur.fetchone()

            if not row:
                return None

            return UserInfo(
                row["id"],
                row["full_name"],
                row["role_name"],
            )

        finally:
            conn.close()

    @staticmethod
    def get_products():
        conn = get_connection()

        try:
            cur = conn.cursor(dictionary=True)

            cur.execute(
                """
                SELECT
                    p.id,
                    p.article,
                    p.name,
                    c.category_name,
                    p.description,
                    m.manufacture_name,
                    s.supplier_name,
                    p.cost,
                    p.measure,
                    p.amount,
                    p.discount,
                    p.photo
                FROM products p
                         JOIN categories c
                              ON c.id = p.category_id
                         JOIN manufacturers m
                              ON m.id = p.manufacture_id
                         JOIN suppliers s
                              ON s.id = p.supplier_id
                ORDER BY p.id
                """
            )

            return cur.fetchall()

        finally:
            conn.close()

    @staticmethod
    def get_supplier_names():
        conn = get_connection()

        try:
            cur = conn.cursor()

            cur.execute(
                """
                SELECT supplier_name
                FROM suppliers
                ORDER BY supplier_name
                """
            )

            return [x[0] for x in cur.fetchall()]

        finally:
            conn.close()

    @staticmethod
    def get_categories():
        conn = get_connection()

        try:
            cur = conn.cursor(dictionary=True)

            cur.execute(
                """
                SELECT
                    id,
                    category_name
                FROM categories
                ORDER BY category_name
                """
            )

            return cur.fetchall()

        finally:
            conn.close()

    @staticmethod
    def get_manufactures():
        conn = get_connection()

        try:
            cur = conn.cursor(dictionary=True)

            cur.execute(
                """
                SELECT
                    id,
                    manufacture_name
                FROM manufacturers
                ORDER BY manufacture_name
                """
            )

            return cur.fetchall()

        finally:
            conn.close()

    @staticmethod
    def get_product_by_id(product_id: int):
        conn = get_connection()

        try:
            cur = conn.cursor(dictionary=True)

            cur.execute(
                """
                SELECT p.id,
                       p.article,
                       p.name,
                       p.category_id,
                       p.description,
                       p.manufacture_id,
                       p.supplier_id,
                       s.supplier_name,
                       p.cost,
                       p.measure,
                       p.amount,
                       p.discount,
                       p.photo
                FROM products p
                         JOIN suppliers s
                              ON s.id = p.supplier_id
                WHERE p.id = %s
                """,
                (product_id,),
            )

            return cur.fetchone()

        finally:
            conn.close()

    @staticmethod
    def ensure_supplier(conn, supplier_name: str):
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id
            FROM suppliers
            WHERE supplier_name = %s
            """,
            (supplier_name,),
        )

        row = cur.fetchone()

        if row:
            return row[0]

        cur.execute(
            """
            INSERT INTO suppliers(supplier_name)
            VALUES(%s)
            """,
            (supplier_name,),
        )

        conn.commit()

        return cur.lastrowid

    @staticmethod
    def save_product(model: dict):
        conn = get_connection()

        try:
            supplier_id = DataService.ensure_supplier(
                conn,
                model["supplier_name"],
            )

            cur = conn.cursor()

            if model.get("id"):

                cur.execute(
                    """
                    UPDATE products
                    SET
                        article=%s,
                        name=%s,
                        measure=%s,
                        cost=%s,
                        supplier_id=%s,
                        manufacture_id=%s,
                        category_id=%s,
                        discount=%s,
                        amount=%s,
                        description=%s,
                        photo=%s
                    WHERE id=%s
                    """,
                    (
                        model["article"],
                        model["name"],
                        model["measure"],
                        model["cost"],
                        supplier_id,
                        model["manufacture_id"],
                        model["category_id"],
                        model["discount"],
                        model["amount"],
                        model["description"],
                        model["photo"],
                        model["id"],
                    ),
                )

            else:

                cur.execute(
                    """
                    INSERT INTO products(
                        article,
                        name,
                        measure,
                        cost,
                        supplier_id,
                        manufacture_id,
                        category_id,
                        discount,
                        amount,
                        description,
                        photo
                    )
                    VALUES(
                              %s,%s,%s,%s,%s,
                              %s,%s,%s,%s,%s,%s
                          )
                    """,
                    (
                        model["article"],
                        model["name"],
                        model["measure"],
                        model["cost"],
                        supplier_id,
                        model["manufacture_id"],
                        model["category_id"],
                        model["discount"],
                        model["amount"],
                        model["description"],
                        model["photo"],
                    ),
                )

            conn.commit()

        finally:
            conn.close()

    @staticmethod
    def delete_product(product_id: int):
        conn = get_connection()

        try:
            cur = conn.cursor()

            cur.execute(
                """
                DELETE FROM products
                WHERE id = %s
                """,
                (product_id,),
            )

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
                SELECT
                    oi.id,
                    oi.product_id,
                    oi.quantity,
                    p.article,
                    p.name,
                    p.cost
                FROM order_items oi
                         JOIN products p
                              ON p.id = oi.product_id
                WHERE oi.order_id = %s
                ORDER BY p.name
                """,
                (order_id,),
            )

            return cur.fetchall()

        finally:
            conn.close()

    @staticmethod
    def get_orders():
        conn = get_connection()

        try:
            cur = conn.cursor(dictionary=True)

            cur.execute(
                """
                SELECT
                    o.id,
                    o.code,
                    o.order_date,
                    o.ship_date,
                    o.address_id,
                    o.user_id,
                    s.status_name,
                    a.city_name,
                    a.street_name,
                    a.house_number,
                    a.address_index
                FROM orders o
                         JOIN order_statuses s
                              ON s.id = o.status_id
                         JOIN addresses a
                              ON a.id = o.address_id
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

            cur.execute(
                """
                SELECT *
                FROM orders
                WHERE id = %s
                """,
                (order_id,),
            )

            return cur.fetchone()

        finally:
            conn.close()

    @staticmethod
    def get_order_statuses():
        conn = get_connection()

        try:
            cur = conn.cursor(dictionary=True)

            cur.execute(
                """
                SELECT id, status_name
                FROM order_statuses
                ORDER BY status_name
                """
            )

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
                SELECT
                    id,
                    address_index,
                    city_name,
                    street_name,
                    house_number
                FROM addresses
                ORDER BY id
                """
            )

            return cur.fetchall()

        finally:
            conn.close()

    @staticmethod
    def get_next_code():
        conn = get_connection()

        try:
            cur = conn.cursor()

            cur.execute(
                """
                SELECT COALESCE(MAX(code), 900) + 1
                FROM orders
                """
            )

            return cur.fetchone()[0]

        finally:
            conn.close()

    @staticmethod
    def save_order(model: dict):
        conn = get_connection()

        try:
            cur = conn.cursor()

            if model.get("id"):

                cur.execute(
                    """
                    UPDATE orders
                    SET
                        address_id = %s,
                        status_id = %s,
                        order_date = %s,
                        ship_date = %s
                    WHERE id = %s
                    """,
                    (
                        model["address_id"],
                        model["status_id"],
                        model["order_date"],
                        model["ship_date"],
                        model["id"],
                    ),
                )

                order_id = model["id"]

                cur.execute(
                    """
                    DELETE FROM order_items
                    WHERE order_id = %s
                    """,
                    (order_id,),
                )

            else:

                cur.execute(
                    """
                    INSERT INTO orders(
                        address_id,
                        user_id,
                        code,
                        status_id,
                        order_date,
                        ship_date
                    )
                    VALUES(%s,%s,%s,%s,%s,%s)
                    """,
                    (
                        model["address_id"],
                        None,
                        model["code"],
                        model["status_id"],
                        model["order_date"],
                        model["ship_date"],
                    ),
                )

                order_id = cur.lastrowid

            for item in model["items"]:

                cur.execute(
                    """
                    INSERT INTO order_items(
                        order_id,
                        product_id,
                        quantity
                    )
                    VALUES(%s,%s,%s)
                    """,
                    (
                        order_id,
                        item["product_id"],
                        item["quantity"],
                    ),
                )

            conn.commit()

        finally:
            conn.close()

    @staticmethod
    def delete_order(order_id: int):
        conn = get_connection()

        try:
            cur = conn.cursor()

            cur.execute(
                """
                DELETE FROM orders
                WHERE id = %s
                """,
                (order_id,),
            )

            conn.commit()

        finally:
            conn.close()