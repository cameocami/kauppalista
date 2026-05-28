import db

def add_product(name, price, user_id):
    sql = "INSERT INTO products (name, price, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [name, price, user_id])

def get_products():
    sql = "SELECT id, name FROM products ORDER BY id DESC"
    return db.query(sql)

def get_product(product_id):
    sql = """   SELECT      products.name,
                            products.price,
                            users.username
                FROM        products, users
                WHERE   products.user_id = users.id AND
                        products.id = ? """
    return db.query(sql, [product_id])[0]