INSERT INTO order_items (order_id, product_id, quantity)
SELECT o.order_id,
       pr.id,
       CAST(TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(o.data_text, ',', 2), ',', -1)) AS UNSIGNED) AS qty
FROM orders_items_raw o
         JOIN products pr ON pr.article = TRIM(SUBSTRING_INDEX(o.data_text, ',', 1))
WHERE TRIM(o.data_text) <> '';

-- -----------------

INSERT INTO order_items (order_id, product_id, quantity)
SELECT o.order_id,
       pr.id,
       CAST(TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(o.data_text, ',', 4), ',', -1)) AS UNSIGNED) AS qty
FROM orders_items_raw o
         JOIN products pr
              ON pr.article = TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(o.data_text, ',', 3), ',', -1))
WHERE TRIM(o.data_text) <> '';

-- DATE SHIT


UPDATE `orders`
SET `order_date`=STR_TO_DATE(TRIM(order_date), '%d.%m.%Y'),
    `ship_date`=STR_TO_DATE(TRIM(ship_date), '%d.%m.%Y')
    WHERE 1=1;

alter table orders modify order_date DATE;
alter table orders modify ship_date DATE;
