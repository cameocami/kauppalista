DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS units;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS shopping_lists;
DROP TABLE IF EXISTS shopping_list_items;
DROP TABLE IF EXISTS product_ratings;

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name TEXT,
    display_name TEXT
);

CREATE TABLE units (
    id INTEGER PRIMARY KEY,
    name TEXT,
    display_name TEXT
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price DECIMAL(10,2),
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    unit_id INTEGER REFERENCES units,
    department_id INTEGER REFERENCES departments
);

CREATE TABLE shopping_lists (
    id INTEGER PRIMARY KEY,
    name TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE shopping_list_items (
    id INTEGER PRIMARY KEY,
    shopping_list_id INTEGER REFERENCES shopping_lists ON DELETE CASCADE,
    product_id INTEGER REFERENCES products ON DELETE CASCADE,
    amount DECIMAL(10,2) NOT NULL
);

CREATE TABLE product_ratings (
    id INTEGER PRIMARY KEY,
    product_id INTEGER REFERENCES products ON DELETE CASCADE,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    rating INTEGER
);

CREATE INDEX idx_products_user_id ON products(user_id);
CREATE INDEX idx_products_unit_id ON products(unit_id);
CREATE INDEX idx_products_department_id ON products(department_id);
