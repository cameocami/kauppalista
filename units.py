import db

def get_unit(unit_name):
    sql = "SELECT id FROM units WHERE name = ?"
    result = db.query(sql, [unit_name])
    return result[0] if result else None