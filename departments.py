import db

def get_department_id(department_name):
    sql = "SELECT id FROM departments WHERE departments.name = ?"
    result = db.query(sql, [department_name])
    return result[0][0] if result else get_department_id("other")

def get_all_departments():
    sql = "SELECT name, display_name FROM departments ORDER BY id"
    result = db.query(sql)
    return result

