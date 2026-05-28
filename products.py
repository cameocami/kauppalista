import db

def add_item(name, price, user_id):
    sql = "INSERT INTO products (name, price, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [name, price, user_id])