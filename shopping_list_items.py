import db
def is_on_list(product_id, shopping_list_id):
    sql = """ SELECT product_id FROM shopping_list_items WHERE product_id = ? AND shopping_list_id = ?
            """
    result = db.query(sql, [product_id, shopping_list_id])
    return True if result else False

def amount(product_id, shopping_list_id):
    sql = "SELECT amount FROM shopping_list_items WHERE product_id = ? AND shopping_list_id = ?"
    result = db.query(sql, [product_id, shopping_list_id])
    return int(result[0][0]) if result else None

def add_new(shopping_list_id, product_id, amount):
    sql = """INSERT INTO shopping_list_items
        (shopping_list_id, product_id, amount)
        VALUES (?, ?, ?)"""
    db.execute(sql, [shopping_list_id, product_id, amount])

def update_amount(amount, shopping_list_id, product_id):
    sql = """   UPDATE shopping_list_items
                SET amount = ?
                WHERE shopping_list_id = ? AND product_id = ?"""
    db.execute(sql, [amount, shopping_list_id, product_id])

def get_items(shopping_list_id):
    sql = """SELECT products.name AS name,
                    products.id AS id,
                    products.price AS price,
                    shopping_list_items.amount AS amount,
                    units.name AS unit,
                    units.display_name AS unit_display_name,
                    departments.name AS department,
                    departments.display_name AS department_display_name
            FROM shopping_list_items
            JOIN products ON shopping_list_items.product_id = products.id
            JOIN units ON products.unit_id = units.id
            JOIN departments ON products.department_id = departments.id       
            WHERE shopping_list_id = ?
            ORDER BY shopping_list_items.id"""
    result = db.query(sql, [shopping_list_id])
    return result

def remove_product_from_all(product_id):
    sql = " DELETE FROM shopping_list_items WHERE product_id = ?"
    db.execute(sql, [product_id])