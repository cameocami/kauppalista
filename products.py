import db

def add_product(name, price, user_id, unit_id, department_id):
    sql = """INSERT INTO products
        (name, price, user_id, unit_id, department_id)
        VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [name, price, user_id, unit_id, department_id])
    return db.last_insert_id()

def get_products(page, page_size):
    sql = """   SELECT  products.id,
                        products.name,
                        units.display_name AS unit
                FROM    products,
                        units
                WHERE   products.unit_id = units.id
                ORDER BY products.id DESC
                LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

def get_product(product_id):
    sql = """   SELECT      products.id,
                            products.name,
                            printf("%.2f", products.price) AS price,
                            users.id AS user_id,
                            users.username,
                            units.display_name AS unit,
                            departments.display_name AS department
                FROM        products
                LEFT JOIN   users ON products.user_id = users.id
                LEFT JOIN   units ON units.id = products.unit_id
                LEFT JOIN   departments ON departments.id = products.department_id
                WHERE       products.id = ?"""
    result = db.query(sql, [product_id])
    return result[0] if result else None

def update_product(product_id, name, price, unit_id, department_id):
    sql = """   UPDATE products
                SET name = ?, price = ?, unit_id = ?, department_id = ?
                WHERE id = ? """
    db.execute(sql, [name, price, unit_id, department_id, product_id])

def remove_product(product_id):
    sql = "DELETE FROM products WHERE id = ?"
    db.execute(sql, [product_id])

def find_products(query):
    sql = """SELECT products.id AS id, products.name AS name, units.display_name AS unit
            FROM products
            JOIN units ON units.id = products.unit_id
            WHERE products.name LIKE ?
            ORDER BY id DESC"""
    return db.query(sql, ["%" + query + "%"])

def product_count():
    sql = "SELECT COUNT(*) FROM products"
    result = db.query(sql)
    return result[0][0] if result else None

def exists(product_id):
    sql = "SELECT id FROM products WHERE id = ?"
    result = db.query(sql, [product_id])
    return bool(result)

def get_owner(product_id):
    sql = "SELECT user_id FROM products WHERE id = ?"
    result = db.query(sql, [product_id])
    return result[0][0]
