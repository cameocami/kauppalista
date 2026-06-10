import db
import shopping_list_items

def add_product(name, price, user_id, unit_id, department_id):
    sql = """INSERT INTO products
        (name, price, user_id, unit_id, department_id)
        VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [name, price, user_id, unit_id, department_id])

def get_products():
    sql = """   SELECT  products.id,
                        products.name,
                        units.display_name AS unit
                FROM    products,
                        units
                WHERE   products.unit_id = units.id
                ORDER BY products.id DESC"""
    return db.query(sql)

def get_product(product_id):
    sql = """   SELECT      products.id,
                            products.name,
                            printf("%.2f", products.price) AS price,
                            users.id AS user_id,
                            users.username,
                            units.display_name AS unit,
                            departments.display_name AS department
                FROM        products
                JOIN        users ON products.user_id = users.id
                JOIN        units ON units.id = products.unit_id
                JOIN        departments ON departments.id = products.department_id
                WHERE       products.id = ?"""
    result = db.query(sql, [product_id])
    return result[0] if result else None

def update_product(product_id, name, price, unit_id, department_id):
    sql = """   UPDATE products
                SET name = ?, price = ?, unit_id = ?, department_id = ?
                WHERE id = ? """
    db.execute(sql, [name, price, unit_id, department_id, product_id])

def remove_product(product_id):
    shopping_list_items.remove_product_from_all(product_id)
    sql = "DELETE FROM products WHERE id = ?"
    db.execute(sql, [product_id])

def find_products(query):
    sql = """SELECT id, name
            FROM products
            WHERE name LIKE ?
            ORDER BY id DESC"""
    return db.query(sql, ["%" + query + "%"])
