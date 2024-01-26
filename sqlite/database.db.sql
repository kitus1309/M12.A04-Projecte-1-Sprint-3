BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "banned_products" (
	"product_id"	INTEGER,
	"reason"	TEXT NOT NULL,
	"created"	DATETIME NOT NULL DEFAULT (DATETIME('now')),
	FOREIGN KEY("product_id") REFERENCES "products"("id"),
	PRIMARY KEY("product_id")
);
CREATE TABLE IF NOT EXISTS "blocked_users" (
	"user_id"	INTEGER,
	"message"	TEXT NOT NULL,
	"created"	DATETIME NOT NULL DEFAULT (DATETIME('now')),
	FOREIGN KEY("user_id") REFERENCES "users"("id"),
	PRIMARY KEY("user_id")
);
CREATE TABLE IF NOT EXISTS "categories" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL UNIQUE,
	"slug"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "confirmed_orders" (
	"order_id"	INTEGER,
	"created"	DATETIME,
	FOREIGN KEY("order_id") REFERENCES "orders"("id")
);
CREATE TABLE IF NOT EXISTS "orders" (
	"id"	INTEGER,
	"product_id"	INTEGER,
	"buyer_id"	INTEGER,
	"offer"	REAL,
	"created"	DATETIME,
	FOREIGN KEY("product_id") REFERENCES "products"("id"),
	FOREIGN KEY("buyer_id") REFERENCES "users"("id"),
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "products" (
	"id"	INTEGER,
	"title"	TEXT NOT NULL,
	"description"	TEXT NOT NULL,
	"photo"	TEXT NOT NULL,
	"price"	DECIMAL(10, 2) NOT NULL,
	"category_id"	INTEGER NOT NULL,
	"status_id"	INTEGER NOT NULL,
	"seller_id"	INTEGER NOT NULL,
	"created"	DATETIME NOT NULL DEFAULT (DATETIME('now')),
	"updated"	DATETIME NOT NULL DEFAULT (DATETIME('now')),
	FOREIGN KEY("category_id") REFERENCES "categories"("id"),
	FOREIGN KEY("status_id") REFERENCES "statuses"("id"),
	FOREIGN KEY("seller_id") REFERENCES "users"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "statuses" (
	"id"	INTEGER,
	"name"	TEXT UNIQUE,
	"slug"	TEXT UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "users" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL UNIQUE,
	"email"	TEXT NOT NULL UNIQUE,
	"role"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	"email_token"	TEXT DEFAULT NULL,
	"verified"	INTEGER NOT NULL DEFAULT FALSE,
	"created"	DATETIME NOT NULL DEFAULT (DATETIME('now')),
	"updated"	DATETIME NOT NULL DEFAULT (DATETIME('now')),
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "categories" ("id","name","slug") VALUES (1,'Electrònica','electronica');
INSERT INTO "categories" ("id","name","slug") VALUES (2,'Roba','roba');
INSERT INTO "categories" ("id","name","slug") VALUES (4,'Joguines','joguines');
INSERT INTO "orders" ("id","product_id","buyer_id","offer","created") VALUES (1,6,5,20.0,'2024-01-26 15:12:05');
INSERT INTO "products" ("id","title","description","photo","price","category_id","status_id","seller_id","created","updated") VALUES (6,'Televisio','Una tele gran','no_image.png',33,1,1,5,'2024-01-26 15:12:05','2024-01-26 15:12:05');
INSERT INTO "products" ("id","title","description","photo","price","category_id","status_id","seller_id","created","updated") VALUES (7,'Camiseta','Una camiseta roja','no_image.png',23,2,1,5,'2024-01-26 15:12:32','2024-01-26 15:12:32');
INSERT INTO "products" ("id","title","description","photo","price","category_id","status_id","seller_id","created","updated") VALUES (8,'Telèfon mòbil','Un telèfon intel·ligent d''''última generació.','no_image.png',599.99,1,1,5,'2024-01-26 15:14:12','2024-01-26 15:14:12');
INSERT INTO "statuses" ("id","name","slug") VALUES (1,'Nou','nou');
INSERT INTO "statuses" ("id","name","slug") VALUES (2,'Usat','usat');
INSERT INTO "users" ("id","name","email","role","password","email_token","verified","created","updated") VALUES (1,'Joan Pérez','joan@example.com','admin','scrypt:32768:8:1$lwqNpblQ9OiKBfeM$4d63ebdf494cc8e363f14494bca1c5246f6689b45904431f69fbcb535b7e41bd012e9b41c850125d7f8b790cb320579a46427b69eda892517669eba0244b77b4',NULL,1,'2023-12-10 08:20:25','2023-12-10 08:20:25');
INSERT INTO "users" ("id","name","email","role","password","email_token","verified","created","updated") VALUES (2,'Anna García','anna@example.com','moderator','scrypt:32768:8:1$lwqNpblQ9OiKBfeM$4d63ebdf494cc8e363f14494bca1c5246f6689b45904431f69fbcb535b7e41bd012e9b41c850125d7f8b790cb320579a46427b69eda892517669eba0244b77b4',NULL,1,'2023-12-10 08:20:25','2023-12-10 08:20:25');
INSERT INTO "users" ("id","name","email","role","password","email_token","verified","created","updated") VALUES (3,'Elia Rodríguez','elia@example.com','wanner','scrypt:32768:8:1$lwqNpblQ9OiKBfeM$4d63ebdf494cc8e363f14494bca1c5246f6689b45904431f69fbcb535b7e41bd012e9b41c850125d7f8b790cb320579a46427b69eda892517669eba0244b77b4',NULL,1,'2023-12-10 08:20:25','2023-12-10 08:20:25');
INSERT INTO "users" ("id","name","email","role","password","email_token","verified","created","updated") VALUES (4,'Kevin Salardú','kevin@example.com','wanner','scrypt:32768:8:1$lwqNpblQ9OiKBfeM$4d63ebdf494cc8e363f14494bca1c5246f6689b45904431f69fbcb535b7e41bd012e9b41c850125d7f8b790cb320579a46427b69eda892517669eba0244b77b4',NULL,1,'2023-12-10 08:20:25','2023-12-10 08:20:25');
INSERT INTO "users" ("id","name","email","role","password","email_token","verified","created","updated") VALUES (5,'claudiu','clvl@fp.insjoaquimmir.cat','wanner','scrypt:32768:8:1$eebvVIfPMhFMJxEC$18d2f866271bdcfdd5bda24a617fd4d94dbce577463b1a0a37a90288c490b0c8264a387f700950540dd4ac003eaaff9c350e4cdef0e8049050c847afe31fd514','Nwi6umy5jMgvmRmurN3r168FL0o',1,'2024-01-19 16:34:30','2024-01-19 16:34:30');
COMMIT;
