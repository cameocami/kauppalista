import db

def get_unit_id(unit_name):
    sql = "SELECT id FROM units WHERE name = ?"
    result = db.query(sql, [unit_name])
    return result[0][0] if result else None

def get_all_units():
    sql = "SELECT name, display_name FROM units ORDER BY id"
    result = db.query(sql)
    return result
