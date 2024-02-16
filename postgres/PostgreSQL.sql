DROP TABLE IF EXISTS "banned_products";
CREATE TABLE "public"."banned_products" (
    "product_id" integer NOT NULL,
    "reason" text,
    "created" timestamp DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "banned_products_pkey" PRIMARY KEY ("product_id")
) WITH (oids = false);


DROP TABLE IF EXISTS "blocked_users";
CREATE TABLE "public"."blocked_users" (
    "user_id" integer NOT NULL,
    "message" text,
    "created" timestamp DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "blocked_users_pkey" PRIMARY KEY ("user_id")
) WITH (oids = false);


DROP TABLE IF EXISTS "categories";
DROP SEQUENCE IF EXISTS categories_id_seq;
CREATE SEQUENCE categories_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."categories" (
    "id" integer DEFAULT nextval('categories_id_seq') NOT NULL,
    "name" text,
    "slug" text,
    CONSTRAINT "categories_name_key" UNIQUE ("name"),
    CONSTRAINT "categories_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "categories_slug_key" UNIQUE ("slug")
) WITH (oids = false);

INSERT INTO "categories" ("id", "name", "slug") VALUES
(1,	'Electrònica',	'electronica'),
(2,	'Roba',	'roba'),
(4,	'Joguines',	'joguines');

DROP TABLE IF EXISTS "confirmed_orders";
CREATE TABLE "public"."confirmed_orders" (
    "order_id" integer NOT NULL,
    "created" timestamp DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "confirmed_orders_pkey" PRIMARY KEY ("order_id")
) WITH (oids = false);


DROP TABLE IF EXISTS "orders";
DROP SEQUENCE IF EXISTS orders_id_seq;
CREATE SEQUENCE orders_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."orders" (
    "id" integer DEFAULT nextval('orders_id_seq') NOT NULL,
    "product_id" integer,
    "buyer_id" integer,
    "offer" numeric,
    "created" timestamp DEFAULT CURRENT_TIMESTAMP,
    "confirmed" boolean NOT NULL,
    CONSTRAINT "orders_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "products";
DROP SEQUENCE IF EXISTS products_id_seq;
CREATE SEQUENCE products_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."products" (
    "id" integer DEFAULT nextval('products_id_seq') NOT NULL,
    "title" text,
    "description" text,
    "photo" text,
    "price" numeric(10,2),
    "category_id" integer,
    "seller_id" integer,
    "created" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "updated" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "status_id" integer NOT NULL,
    CONSTRAINT "products_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

INSERT INTO "products" ("id", "title", "description", "photo", "price", "category_id", "seller_id", "created", "updated", "status_id") VALUES
(7,	'Camiseta',	'Una camiseta roja',	'no_image.png',	23.00,	2,	5,	'2024-01-26 15:12:32',	'2024-01-26 15:12:32',	1),
(8,	'Telèfon mòbil',	'Un telèfon intel·ligent d''última generació.',	'no_image.png',	599.99,	1,	5,	'2024-01-26 15:14:12',	'2024-01-26 15:14:12',	1),
(9,	'Test',	'kdsakkd',	'no_image.png',	132.00,	1,	4,	'2024-02-02 19:46:48',	'2024-02-02 19:46:48',	1),
(10,	'Test put',	'Prueba put',	'Test.png',	29.99,	2,	3,	'2024-02-09 15:05:07',	'2024-02-09 16:09:01',	1);

DROP TABLE IF EXISTS "sqlite_sequence";
CREATE TABLE "public"."sqlite_sequence" (
    "name" text,
    "seq" integer
) WITH (oids = false);


DROP TABLE IF EXISTS "statuses";
DROP SEQUENCE IF EXISTS statuses_id_seq;
CREATE SEQUENCE statuses_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."statuses" (
    "id" integer DEFAULT nextval('statuses_id_seq') NOT NULL,
    "name" text,
    "slug" text,
    CONSTRAINT "statuses_name_key" UNIQUE ("name"),
    CONSTRAINT "statuses_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "statuses_slug_key" UNIQUE ("slug")
) WITH (oids = false);

INSERT INTO "statuses" ("id", "name", "slug") VALUES
(1,	'Nou',	'nou'),
(2,	'Usat',	'usat'),
(3,	'En Proceso',	'en-proceso'),
(4,	'Vendido',	'vendido');

DROP TABLE IF EXISTS "users";
DROP SEQUENCE IF EXISTS users_id_seq;
CREATE SEQUENCE users_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."users" (
    "id" integer DEFAULT nextval('users_id_seq') NOT NULL,
    "name" text,
    "email" text,
    "password" text,
    "created" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "updated" timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "role" text,
    "email_token" text,
    "verified" integer,
    "token" text,
    "token_expiration" timestamp,
    CONSTRAINT "users_email_key" UNIQUE ("email"),
    CONSTRAINT "users_name_key" UNIQUE ("name"),
    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

INSERT INTO "users" ("id", "name", "email", "password", "created", "updated", "role", "email_token", "verified", "token", "token_expiration") VALUES
(1,	'Joan Pérez',	'joan@example.com',	'scrypt:32768:8:1$lwqNpblQ9OiKBfeM$4d63ebdf494cc8e363f14494bca1c5246f6689b45904431f69fbcb535b7e41bd012e9b41c850125d7f8b790cb320579a46427b69eda892517669eba0244b77b4',	'2023-12-10 08:20:25',	'2024-02-09 14:46:43',	'admin',	NULL,	1,	'1d8d25ac8f8faebb44b3e30ba23adb37',	'2024-02-09 15:46:43.178828'),
(2,	'Anna García',	'anna@example.com',	'scrypt:32768:8:1$lwqNpblQ9OiKBfeM$4d63ebdf494cc8e363f14494bca1c5246f6689b45904431f69fbcb535b7e41bd012e9b41c850125d7f8b790cb320579a46427b69eda892517669eba0244b77b4',	'2023-12-10 08:20:25',	'2023-12-10 08:20:25',	'moderator',	NULL,	1,	NULL,	NULL),
(3,	'Elia Rodríguez',	'elia@example.com',	'scrypt:32768:8:1$lwqNpblQ9OiKBfeM$4d63ebdf494cc8e363f14494bca1c5246f6689b45904431f69fbcb535b7e41bd012e9b41c850125d7f8b790cb320579a46427b69eda892517669eba0244b77b4',	'2023-12-10 08:20:25',	'2024-02-09 15:28:22',	'wanner',	NULL,	1,	'a12f8cb0e26fcd0b9abda23ca547c5ea',	'2024-02-09 16:28:22.459936'),
(4,	'Kevin Salardú',	'kevin@example.com',	'scrypt:32768:8:1$lwqNpblQ9OiKBfeM$4d63ebdf494cc8e363f14494bca1c5246f6689b45904431f69fbcb535b7e41bd012e9b41c850125d7f8b790cb320579a46427b69eda892517669eba0244b77b4',	'2023-12-10 08:20:25',	'2024-02-02 19:52:19',	'wanner',	NULL,	1,	'83a73f6e9cd858122e1a521f7ca8273c',	'2024-02-02 19:52:18.634092'),
(5,	'claudiu',	'clvl@fp.insjoaquimmir.cat',	'scrypt:32768:8:1$eebvVIfPMhFMJxEC$18d2f866271bdcfdd5bda24a617fd4d94dbce577463b1a0a37a90288c490b0c8264a387f700950540dd4ac003eaaff9c350e4cdef0e8049050c847afe31fd514',	'2024-01-19 16:34:30',	'2024-02-09 15:04:22',	'wanner',	'Nwi6umy5jMgvmRmurN3r168FL0o',	1,	'9836146ae7ca21cfb34378f179f3bb8f',	'2024-02-09 15:04:21.246987');

ALTER TABLE ONLY "public"."banned_products" ADD CONSTRAINT "banned_products_product_id_fkey" FOREIGN KEY (product_id) REFERENCES products(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."blocked_users" ADD CONSTRAINT "blocked_users_user_id_fkey" FOREIGN KEY (user_id) REFERENCES users(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."confirmed_orders" ADD CONSTRAINT "confirmed_orders_order_id_fkey" FOREIGN KEY (order_id) REFERENCES orders(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."orders" ADD CONSTRAINT "orders_buyer_id_fkey" FOREIGN KEY (buyer_id) REFERENCES users(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."orders" ADD CONSTRAINT "orders_product_id_fkey" FOREIGN KEY (product_id) REFERENCES products(id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."products" ADD CONSTRAINT "products_category_id_fkey" FOREIGN KEY (category_id) REFERENCES categories(id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."products" ADD CONSTRAINT "products_seller_id_fkey" FOREIGN KEY (seller_id) REFERENCES users(id) NOT DEFERRABLE;