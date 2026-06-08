DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS units;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS shopping_lists;
DROP TABLE IF EXISTS shopping_list_items;

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
    price FLOAT,
    user_id INTEGER REFERENCES users,
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
    shopping_list_id INTEGER REFERENCES shopping_lists,
    product_id INTEGER REFERENCES products,
    amount INTEGER NOT NULL
);