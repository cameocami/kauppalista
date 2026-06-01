import db

def get_department(department_name):
    sql = "SELECT departments.id FROM departments WHERE departments.name = ?"
    result = db.query(sql, [department_name])
    return result[0] if result else None
