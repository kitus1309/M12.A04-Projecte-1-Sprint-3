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
	"confirmed"	BOOLEAN DEFAULT 0,
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
	"token"	VARCHAR,
	"token_expiration"	DATETIME,
	PRIMARY KEY("id" AUTOINCREMENT)
);
COMMIT;
