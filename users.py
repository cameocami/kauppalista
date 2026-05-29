import db

def get_users():
    sql = "SELECT id, username FROM users ORDER BY id DESC"
    return db.query(sql)

def get_user(user_id):
    sql = """   SELECT      id,
                            username
                FROM        users
                WHERE       id = ?"""
    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_products(user_id):
    sql = """   SELECT      id,
                            name
                FROM        products
                WHERE       user_id = ?"""
    return db.query(sql, [user_id])