-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Хост: mysql:3307
-- Время создания: Июн 03 2026 г., 14:27
-- Версия сервера: 8.4.9
-- Версия PHP: 8.3.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `dem_database`
--

-- --------------------------------------------------------

--
-- Структура таблицы `addresses`
--

CREATE TABLE `addresses` (
  `id` int NOT NULL,
  `address_index` int NOT NULL,
  `city_name` varchar(255) NOT NULL,
  `street_name` varchar(255) NOT NULL,
  `house_number` tinyint NOT NULL
) ;

--
-- Дамп данных таблицы `addresses`
--

INSERT INTO `addresses` (`id`, `address_index`, `city_name`, `street_name`, `house_number`) VALUES
(1, 420151, ' г. Лесной', ' ул. Вишневая', 32),
(2, 125061, ' г. Лесной', ' ул. Подгорная', 8),
(3, 630370, ' г. Лесной', ' ул. Шоссейная', 24),
(4, 400562, ' г. Лесной', ' ул. Зеленая', 32),
(5, 614510, ' г. Лесной', ' ул. Маяковского', 47),
(6, 410542, ' г. Лесной', ' ул. Светлая', 46),
(7, 620839, ' г. Лесной', ' ул. Цветочная', 8),
(8, 443890, ' г. Лесной', ' ул. Коммунистическая', 1),
(9, 603379, ' г. Лесной', ' ул. Спортивная', 46),
(10, 603721, ' г. Лесной', ' ул. Гоголя', 41),
(11, 410172, ' г. Лесной', ' ул. Северная', 13),
(12, 614611, ' г. Лесной', ' ул. Молодежная', 50),
(13, 454311, ' г. Лесной', ' ул. Новая', 19),
(14, 660007, ' г. Лесной', ' ул. Октябрьская', 19),
(15, 603036, ' г. Лесной', ' ул. Садовая', 4),
(16, 394060, ' г. Лесной', ' ул. Фрунзе', 43),
(17, 410661, ' г. Лесной', ' ул. Школьная', 50),
(18, 625590, ' г. Лесной', ' ул. Коммунистическая', 20),
(19, 625683, ' г. Лесной', ' ул. 8 Марта', 11),
(20, 450983, ' г. Лесной', ' ул. Комсомольская', 26),
(21, 394782, ' г. Лесной', ' ул. Чехова', 3),
(22, 603002, ' г. Лесной', ' ул. Дзержинского', 28),
(23, 450558, ' г. Лесной', ' ул. Набережная', 30),
(24, 344288, ' г. Лесной', ' ул. Чехова', 1),
(25, 614164, ' г. Лесной', ' ул. Степная', 30),
(26, 394242, ' г. Лесной', ' ул. Коммунистическая', 43),
(27, 660540, ' г. Лесной', ' ул. Солнечная', 25),
(28, 125837, ' г. Лесной', ' ул. Шоссейная', 40),
(29, 125703, ' г. Лесной', ' ул. Партизанская', 49),
(30, 625283, ' г. Лесной', ' ул. Победы', 46),
(31, 614753, ' г. Лесной', ' ул. Полевая', 35),
(32, 426030, ' г. Лесной', ' ул. Маяковского', 44),
(33, 450375, ' г. Лесной ', ' ул. Клубная', 44),
(34, 625560, ' г. Лесной', ' ул. Некрасова', 12),
(35, 630201, ' г. Лесной', ' ул. Комсомольская', 17),
(36, 190949, ' г. Лесной', ' ул. Мичурина', 26);

-- --------------------------------------------------------

--
-- Структура таблицы `categories`
--

CREATE TABLE `categories` (
  `id` int NOT NULL,
  `category_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `categories`
--

INSERT INTO `categories` (`id`, `category_name`) VALUES
(5, 'Защита лица, глаз, головы'),
(1, 'Общестроительные материалы'),
(4, 'Ручной инструмент'),
(2, 'Стеновые и фасадные материалы'),
(3, 'Сухие строительные смеси и гидроизоляция');

-- --------------------------------------------------------

--
-- Структура таблицы `manufacturers`
--

CREATE TABLE `manufacturers` (
  `id` int NOT NULL,
  `manufacture_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `manufacturers`
--

INSERT INTO `manufacturers` (`id`, `manufacture_name`) VALUES
(10, 'Armero'),
(16, 'Delta'),
(9, 'Hesler'),
(15, 'Husqvarna'),
(12, 'KILIMGRIN'),
(3, 'Knauf'),
(4, 'MixMaster'),
(14, 'RUIZ'),
(17, 'Vinylon'),
(8, 'Weber'),
(11, 'Wenzo Roma'),
(6, 'ВОЛМА'),
(2, 'Изостронг'),
(13, 'Исток'),
(5, 'ЛСР'),
(1, 'М500'),
(7, 'Павловский завод');

-- --------------------------------------------------------

--
-- Структура таблицы `orders`
--

CREATE TABLE `orders` (
  `id` int NOT NULL,
  `order_date` date DEFAULT NULL,
  `ship_date` date DEFAULT NULL,
  `address_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `code` int NOT NULL,
  `status_id` tinyint NOT NULL
) ;

--
-- Дамп данных таблицы `orders`
--

INSERT INTO `orders` (`id`, `order_date`, `ship_date`, `address_id`, `user_id`, `code`, `status_id`) VALUES
(1, '2025-02-27', '2025-04-20', 1, 7, 901, 1),
(2, '2024-09-28', '2025-04-21', 11, 8, 902, 1),
(3, '2025-03-21', '2025-04-22', 2, 9, 903, 1),
(4, '2025-02-20', '2025-04-23', 11, 10, 904, 1),
(5, '2025-03-17', '2025-04-24', 2, 7, 905, 1),
(6, '2025-03-01', '2025-04-25', 15, 8, 906, 1),
(7, '2025-03-01', '2025-04-26', 3, 9, 907, 1),
(8, '2025-03-31', '2025-04-27', 19, 10, 908, 2),
(9, '2025-04-02', '2025-04-28', 5, 7, 909, 2),
(10, '2025-04-03', '2025-04-29', 19, 10, 910, 2);

-- --------------------------------------------------------

--
-- Структура таблицы `orders_items_raw`
--

CREATE TABLE `orders_items_raw` (
  `order_id` int DEFAULT NULL,
  `data_text` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `orders_items_raw`
--

INSERT INTO `orders_items_raw` (`order_id`, `data_text`) VALUES
(1, 'PMEZMH, 2, BPV4MM, 2'),
(2, 'JVL42J, 1, F895RB, 1'),
(3, '3XBOTN, 10, 3L7RCZ, 10'),
(4, 'S72AM3, 5, 2G3280, 4'),
(5, 'MIO8YV, 2, UER2QD, 2'),
(6, 'ZR70B4, 1, LPDDM4, 1'),
(7, 'LQ48MW, 10, O43COU8, 10'),
(8, 'M26EXW, 5, K0YACK, 4'),
(9, 'ASPXSG, 5, ZKQ5FF, 1'),
(10, '4WZEOT, 5, 4JR1HN, 5');

-- --------------------------------------------------------

--
-- Структура таблицы `order_items`
--

CREATE TABLE `order_items` (
  `id` int NOT NULL,
  `order_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` smallint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `product_id`, `quantity`) VALUES
(1, 1, 53, 2),
(2, 2, 55, 1),
(3, 3, 57, 10),
(4, 4, 59, 5),
(5, 5, 61, 2),
(6, 6, 63, 1),
(7, 7, 65, 10),
(8, 8, 67, 5),
(9, 9, 69, 5),
(10, 10, 71, 5),
(16, 1, 54, 2),
(17, 2, 56, 1),
(18, 3, 58, 10),
(19, 4, 60, 4),
(20, 5, 62, 2),
(21, 6, 64, 1),
(22, 8, 68, 4),
(23, 9, 70, 1),
(24, 10, 72, 5);

-- --------------------------------------------------------

--
-- Структура таблицы `order_statuses`
--

CREATE TABLE `order_statuses` (
  `id` tinyint NOT NULL,
  `status_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `order_statuses`
--

INSERT INTO `order_statuses` (`id`, `status_name`) VALUES
(1, 'Завершен'),
(2, 'Новый');

-- --------------------------------------------------------

--
-- Структура таблицы `products`
--

CREATE TABLE `products` (
  `id` int NOT NULL,
  `article` varchar(6) NOT NULL,
  `name` varchar(255) NOT NULL,
  `measure` varchar(255) NOT NULL,
  `cost` decimal(10,2) NOT NULL,
  `supplier_id` int NOT NULL,
  `manufacture_id` int NOT NULL,
  `category_id` int NOT NULL,
  `discount` tinyint NOT NULL,
  `amount` smallint NOT NULL,
  `description` varchar(1024) NOT NULL,
  `photo` varchar(255) NOT NULL
) ;

--
-- Дамп данных таблицы `products`
--

INSERT INTO `products` (`id`, `article`, `name`, `measure`, `cost`, `supplier_id`, `manufacture_id`, `category_id`, `discount`, `amount`, `description`, `photo`) VALUES
(53, 'PMEZMH', 'Цемент', 'шт.', 440.00, 1, 1, 1, 8, 34, 'Цемент Евроцемент М500 Д0 ЦЕМ I 42,5 50 кг', 'PMEZMH.jpg'),
(54, 'BPV4MM', 'Пленка техническая', 'шт.', 8.00, 2, 2, 1, 8, 2, 'Пленка техническая полиэтиленовая Изостронг 60 мк 3 м рукав 1,5 м, пог.м', 'BPV4MM.jpg'),
(55, 'JVL42J', 'Пленка техническая', 'шт.', 13.00, 2, 2, 1, 4, 34, 'Пленка техническая полиэтиленовая Изостронг 100 мк 3 м рукав 1,5 м, пог.м', 'JVL42J.jpg'),
(56, 'F895RB', 'Песок строительный', 'шт.', 102.00, 3, 3, 1, 6, 7, 'Песок строительный 50 кг', 'F895RB.jpg'),
(57, '3XBOTN', 'Керамзит фракция', 'шт.', 110.00, 4, 4, 1, 5, 21, 'Керамзит фракция 10-20 мм 0,05 куб.м', '3XBOTN.jpg'),
(58, '3L7RCZ', 'Газобетон', 'шт.', 7400.00, 5, 5, 2, 2, 20, 'Газобетон ЛСР 100х250х625 мм D400', '3L7RCZ.jpg'),
(59, 'S72AM3', 'Пазогребневая плита ', 'шт.', 500.00, 6, 6, 2, 5, 35, 'Пазогребневая плита ВОЛМА Гидро 667х500х80 мм полнотелая', 'S72AM3.jpg'),
(60, '2G3280', 'Угол наружный', 'шт.', 795.00, 17, 17, 2, 9, 20, 'Угол наружный Vinylon 3050 мм серо-голубой', '2G3280.jpg'),
(61, 'MIO8YV', 'Кирпич', 'шт.', 30.00, 6, 6, 2, 9, 31, 'Кирпич рядовой Боровичи полнотелый М150 250х120х65 мм 1NF', 'MIO8YV.jpg'),
(62, 'UER2QD', 'Скоба для пазогребневой плиты', 'шт.', 25.00, 3, 3, 2, 8, 27, 'Скоба для пазогребневой плиты Knauf С1 120х100 мм', 'UER2QD.jpg'),
(63, 'ZR70B4', 'Кирпич', 'шт.', 16.00, 7, 7, 2, 3, 0, 'Кирпич рядовой силикатный Павловский завод полнотелый М200 250х120х65 мм 1NF', ''),
(64, 'LPDDM4', 'Штукатурка гипсовая', 'шт.', 500.00, 3, 3, 3, 6, 38, 'Штукатурка гипсовая Knauf Ротбанд 30 кг', ''),
(65, 'LQ48MW', 'Штукатурка гипсовая', 'шт.', 462.00, 8, 8, 3, 6, 33, 'Штукатурка гипсовая Knauf МП-75 машинная 30 кг', ''),
(66, 'O43COU', 'Шпаклевка', 'шт.', 750.00, 6, 6, 3, 1, 16, 'Шпаклевка полимерная Weber.vetonit LR + для сухих помещений белая 20 кг', ''),
(67, 'M26EXW', 'Клей для плитки, керамогранита и камня', 'шт.', 340.00, 3, 3, 3, 8, 0, 'Клей для плитки, керамогранита и камня Крепс Усиленный серый (класс С1) 25 кг', ''),
(68, 'K0YACK', 'Смесь цементно-песчаная', 'шт.', 160.00, 4, 4, 3, 8, 19, 'Смесь цементно-песчаная (ЦПС) 300 по ТУ MixMaster Универсал 25 кг', ''),
(69, 'ASPXSG', 'Ровнитель', 'шт.', 711.00, 8, 8, 3, 10, 20, 'Ровнитель (наливной пол) финишный Weber.vetonit 4100 самовыравнивающийся высокопрочный 20 кг', ''),
(70, 'ZKQ5FF', 'Лезвие для ножа ', 'шт.', 65.00, 9, 9, 4, 6, 6, 'Лезвие для ножа Hesler 18 мм прямое (10 шт.)', ''),
(71, '4WZEOT', 'Лезвие для ножа ', 'шт.', 110.00, 10, 10, 4, 6, 17, 'Лезвие для ножа Armero 18 мм прямое (10 шт.)', ''),
(72, '4JR1HN', 'Шпатель', 'шт.', 26.00, 9, 9, 4, 6, 7, 'Шпатель малярный 100 мм с пластиковой ручкой', ''),
(73, 'Z3XFSP', 'Нож строительный ', 'шт.', 63.00, 9, 9, 4, 8, 5, 'Нож строительный Hesler 18 мм с ломающимся лезвием пластиковый корпус', ''),
(74, 'I6MH89', 'Валик', 'шт.', 326.00, 11, 11, 4, 12, 3, 'Валик Wenzo Roma полиакрил 250 мм ворс 18 мм для красок грунтов и антисептиков на водной основе с рукояткой', ''),
(75, '83M5ME', 'Кисть', 'шт.', 122.00, 10, 10, 4, 9, 26, 'Кисть плоская смешанная щетина 100х12 мм для красок и антисептиков на водной основе', ''),
(76, '61PGH3', 'Очки защитные', 'шт.', 184.00, 12, 12, 5, 6, 25, 'Очки защитные Delta Plus KILIMANDJARO (KILIMGRIN) открытые с прозрачными линзами', ''),
(77, 'GN6ICZ', 'Каска защитная ', 'шт.', 154.00, 13, 13, 5, 15, 8, 'Каска защитная Исток (КАС001О) оранжевая', ''),
(78, 'Z3LO0U', 'Очки защитные ', 'шт.', 228.00, 14, 14, 5, 9, 11, 'Очки защитные Delta Plus RUIZ (RUIZ1VI) закрытые с прозрачными линзами', ''),
(79, 'QHNOKR', 'Маска защитная', 'шт.', 251.00, 13, 13, 5, 2, 22, 'Маска защитная Исток (ЩИТ001) ударопрочная и термостойкая', ''),
(80, 'EQ6RKO', 'Подшлемник', 'шт.', 36.00, 15, 15, 5, 17, 22, 'Подшлемник для каски одноразовый', ''),
(81, '81F1WG', 'Каска защитная', 'шт.', 1500.00, 16, 16, 5, 2, 13, 'Каска защитная Delta Plus BASEBALL DIAMOND V UP (DIAM5UPBCFLBS) белая', ''),
(82, '0YGHZ7', 'Очки защитные ', 'шт.', 700.00, 15, 15, 5, 9, 36, 'Очки защитные Husqvarna Clear (5449638-01) открытые с прозрачными линзами', '');

-- --------------------------------------------------------

--
-- Структура таблицы `roles`
--

CREATE TABLE `roles` (
  `id` tinyint UNSIGNED NOT NULL,
  `role_name` varchar(60) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `roles`
--

INSERT INTO `roles` (`id`, `role_name`) VALUES
(3, 'Авторизированный клиент'),
(1, 'Администратор'),
(2, 'Менеджер');

-- --------------------------------------------------------

--
-- Структура таблицы `suppliers`
--

CREATE TABLE `suppliers` (
  `id` int NOT NULL,
  `supplier_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `suppliers`
--

INSERT INTO `suppliers` (`id`, `supplier_name`) VALUES
(10, 'Armero'),
(16, 'Delta'),
(9, 'Hesler'),
(15, 'Husqvarna'),
(12, 'KILIMGRIN'),
(3, 'Knauf'),
(4, 'MixMaster'),
(14, 'RUIZ'),
(17, 'Vinylon'),
(8, 'Weber'),
(11, 'Wenzo Roma'),
(6, 'ВОЛМА'),
(2, 'Изостронг'),
(13, 'Исток'),
(5, 'ЛСР'),
(1, 'М500'),
(7, 'Павловский завод');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `role_id` tinyint UNSIGNED DEFAULT NULL,
  `full_name` varchar(255) NOT NULL,
  `login` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `role_id`, `full_name`, `login`, `password`) VALUES
(1, 1, 'Ворсин Петр Евгеньевич', '94d5ous@gmail.com', 'uzWC67'),
(2, 1, 'Старикова Елена Павловна', 'uth4iz@mail.com', '2L6KZG'),
(3, 1, 'Одинцов Серафим Артёмович', 'yzls62@outlook.com', 'JlFRCZ'),
(4, 2, 'Степанов Михаил Артёмович', '1diph5e@tutanota.com', '8ntwUp'),
(5, 2, 'Ворсин Петр Евгеньевич', 'tjde7c@yahoo.com', 'YOyhfR'),
(6, 2, 'Старикова Елена Павловна', 'wpmrc3do@tutanota.com', 'RSbvHv'),
(7, 3, 'Михайлюк Анна Вячеславовна', '5d4zbu@tutanota.com', 'rwVDh9'),
(8, 3, 'Ситдикова Елена Анатольевна', 'ptec8ym@yahoo.com', 'LdNyos'),
(9, 3, 'Никифорова Весения Николаевна', '1qz4kw@mail.com', 'gynQMT'),
(10, 3, 'Сазонов Руслан Германович', '4np6se@mail.com', 'AtnDjr');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `addresses`
--
ALTER TABLE `addresses`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `address_index` (`address_index`);

--
-- Индексы таблицы `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `category_name` (`category_name`);

--
-- Индексы таблицы `manufacturers`
--
ALTER TABLE `manufacturers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `manufacture_name` (`manufacture_name`);

--
-- Индексы таблицы `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD KEY `address_id_FK` (`address_id`),
  ADD KEY `user_id_FK` (`user_id`),
  ADD KEY `status_id_FK` (`status_id`);

--
-- Индексы таблицы `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `order_id` (`order_id`,`product_id`),
  ADD KEY `order_id_FK` (`order_id`),
  ADD KEY `goods_id_FK` (`product_id`);

--
-- Индексы таблицы `order_statuses`
--
ALTER TABLE `order_statuses`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `status_name` (`status_name`);

--
-- Индексы таблицы `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `article` (`article`),
  ADD KEY `supplier_id_FK` (`supplier_id`),
  ADD KEY `category_id_FK` (`category_id`),
  ADD KEY `manufacturer_id_FK` (`manufacture_id`) USING BTREE;

--
-- Индексы таблицы `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `role_name` (`role_name`);

--
-- Индексы таблицы `suppliers`
--
ALTER TABLE `suppliers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `supplier_name` (`supplier_name`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `login` (`login`),
  ADD KEY `role_id_FK` (`role_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `addresses`
--
ALTER TABLE `addresses`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT для таблицы `manufacturers`
--
ALTER TABLE `manufacturers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT для таблицы `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT для таблицы `order_statuses`
--
ALTER TABLE `order_statuses`
  MODIFY `id` tinyint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `products`
--
ALTER TABLE `products`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT для таблицы `roles`
--
ALTER TABLE `roles`
  MODIFY `id` tinyint UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `suppliers`
--
ALTER TABLE `suppliers`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `address_id_FK` FOREIGN KEY (`address_id`) REFERENCES `addresses` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `status_id_FK` FOREIGN KEY (`status_id`) REFERENCES `order_statuses` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `user_id_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_goods_fk` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `order_items_order_fk` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `category_id_FK` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `supplier_id_FK` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `role_id_FK` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
