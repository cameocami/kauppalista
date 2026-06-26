import db
import shopping_list_items
import product_ratings

def add_product(name, price, user_id, unit_id, department_id):
    sql = """INSERT INTO products
        (name, price, user_id, unit_id, department_id)
        VALUES (?, ?, ?, ?, ?)"""
    db.execute(sql, [name, price, user_id, unit_id, department_id])
    return db.last_insert_id()

def get_products():
    sql = """   SELECT  products.id,
                        products.name,
                        units.display_name AS unit
                FROM    products,
                        units
                WHERE   products.unit_id = units.id
                ORDER BY products.id DESC"""
    return db.query(sql)

def get_product(product_id, user_id=None):
    sql = """   SELECT      products.id,
                            products.name,
                            printf("%.2f", products.price) AS price,
                            users.id AS user_id,
                            users.username,
                            units.display_name AS unit,
                            departments.display_name AS department,
                            COALESCE(AVG(all_ratings.rating), 0) AS average_rating,
                            COALESCE(user_ratings.rating, 0) AS user_rating
                FROM        products
                LEFT JOIN   users ON products.user_id = users.id
                LEFT JOIN   units ON units.id = products.unit_id
                LEFT JOIN   departments ON departments.id = products.department_id
                LEFT JOIN   product_ratings AS all_ratings ON products.id = all_ratings.product_id
                LEFT JOIN   product_ratings AS user_ratings ON products.id = user_ratings.product_id AND user_ratings.user_id = ?
                WHERE       products.id = ?
                GROUP BY    products.id, users.id, units.display_name, departments.display_name"""
    result = db.query(sql, [user_id, product_id])
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
