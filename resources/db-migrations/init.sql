CREATE TABLE IF NOT EXISTS `users` (
    `id` int AUTO_INCREMENT NOT NULL UNIQUE,
    `first_name` varchar(255) NOT NULL,
    `last_name` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL,
    `phone` varchar(255) NOT NULL,
    `address` varchar(255) NOT NULL,
    `username` varchar(255) NOT NULL UNIQUE,
    `hashed_password` varchar(255) NOT NULL,
    `is_active` bool NOT NULL DEFAULT TRUE,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `item` (
    `id` int AUTO_INCREMENT NOT NULL UNIQUE,
    `name` varchar(255) NOT NULL,
    `price` float NOT NULL,
    `stock` int NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `orders` (
    `id` int AUTO_INCREMENT NOT NULL UNIQUE,
    `user_id` int NOT NULL,
    `order_date` date NOT NULL,
    `shipping_address` varchar(255) NOT NULL,
    `status` ENUM('TEMP','CLOSE') NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `order_item` (
    `id` int AUTO_INCREMENT NOT NULL UNIQUE,
    `order_id` int NOT NULL,
    `item_id` int NOT NULL,
    `quantity` int NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE IF NOT EXISTS `favorite_item` (
    `id` int AUTO_INCREMENT NOT NULL UNIQUE,
    `user_id` int NOT NULL,
    `item_id` int NOT NULL,
    PRIMARY KEY (`id`)
);

ALTER TABLE `orders` ADD CONSTRAINT `orders_fk1` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`);
ALTER TABLE `order_item` ADD CONSTRAINT `order_item_fk1` FOREIGN KEY (`order_id`) REFERENCES `orders`(`id`);
ALTER TABLE `order_item` ADD CONSTRAINT `order_item_fk2` FOREIGN KEY (`item_id`) REFERENCES `item`(`id`);
ALTER TABLE `favorite_item` ADD CONSTRAINT `favorite_item_fk1` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`);
ALTER TABLE `favorite_item` ADD CONSTRAINT `favorite_item_fk2` FOREIGN KEY (`item_id`) REFERENCES `item`(`id`);

INSERT INTO item (name, price, stock) VALUES ('shopping bag', 12.99, 50);
INSERT INTO item (name, price, stock) VALUES ('personal bag', 15.49, 30);
INSERT INTO item (name, price, stock) VALUES ('laptop bag', 25.99, 20);

INSERT INTO item (name, price, stock) VALUES ('kitchen chair', 45.00, 15);
INSERT INTO item (name, price, stock) VALUES ('office chair', 89.99, 10);
INSERT INTO item (name, price, stock) VALUES ('dining chair', 55.49, 8);

INSERT INTO item (name, price, stock) VALUES ('bedside lamp', 29.99, 40);
INSERT INTO item (name, price, stock) VALUES ('desk lamp', 39.99, 25);
INSERT INTO item (name, price, stock) VALUES ('floor lamp', 79.99, 12);

INSERT INTO item (name, price, stock) VALUES ('running shoes', 60.00, 25);
INSERT INTO item (name, price, stock) VALUES ('walking shoes', 50.00, 30);
INSERT INTO item (name, price, stock) VALUES ('casual shoes', 45.00, 20);

INSERT INTO item (name, price, stock) VALUES ('wooden table', 150.00, 5);
INSERT INTO item (name, price, stock) VALUES ('glass table', 200.00, 3);
INSERT INTO item (name, price, stock) VALUES ('folding table', 75.00, 10);
