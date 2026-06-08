import db
def add_item(shopping_list_id, product_id, amount):
    sql = """INSERT INTO shopping_list_items
        (shopping_list_id, product_id, amount)
        VALUES (?, ?, ?)"""
    db.execute(sql, [shopping_list_id, product_id, amount])


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

