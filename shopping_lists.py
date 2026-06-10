import db

def add(name, user_id):
    sql = """INSERT INTO shopping_lists
        (name, user_id)
        VALUES (?, ?)"""
    db.execute(sql, [name, user_id])

def get_id(user_id):
    sql = """SELECT id
            FROM shopping_lists 
            WHERE user_id = ?"""
    result = db.query(sql, [user_id])
    return result[0][0] if result else None
