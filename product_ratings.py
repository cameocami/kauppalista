import db

def rate(product_id, user_id, rating):
    user_rating = get_user_rating(product_id, user_id)
    if user_rating:
        sql = """   UPDATE product_ratings
                SET rating = ?
                WHERE id = ? """
        db.execute(sql, [rating, user_rating["id"]])
        print("updated")
    else:
        sql = """INSERT INTO product_ratings
        (product_id, user_id, rating)
        VALUES (?, ?, ?)"""
        db.execute(sql, [product_id, user_id, rating])
        print("added")

def get_user_rating(product_id, user_id):
    sql = """ SELECT id, rating
            FROM product_ratings
            WHERE (product_id = ? AND user_id = ?)
            """
    result = db.query(sql, [product_id, user_id])
    return result[0] if result else None
