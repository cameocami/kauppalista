CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name TEXT
);
INSERT into departments (name) VALUES
      ('uncategorized'),
      ('fresh'),
      ('baked'),
      ('dairy'),
      ('meat_fish'),
      ('ready_to_eat'),
      ('pantry'),
      ('drinks'),
      ('frozen'),
      ('hygiene'),
      ('kids_pets');

CREATE TABLE units (
    id INTEGER PRIMARY KEY,
    name TEXT
);
INSERT into units (name) VALUES
      ('piece'),
      ('kilogram'),
      ('liter');
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price FLOAT,
    user_id INTEGER REFERENCES users,
    unit_id INTEGER REFERENCES units,
    department_id INTEGER REFERENCES departments
);
