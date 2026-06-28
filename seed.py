import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM products")
db.execute("DELETE FROM shopping_lists")
db.execute("DELETE FROM shopping_list_items")
db.execute("DELETE FROM product_ratings")

USER_COUNT = 1000
PRODUCT_COUNT = 10**5
MAX_ITEMS_SHOPPING_LIST = 50
MAX_ITEM_AMOUNT = 10
RATING_COUNT = 10**6

for i in range(1, USER_COUNT + 1):
    result = db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])
    user_id = result.lastrowid
    db.execute("INSERT INTO shopping_lists (user_id) VALUES (?)",
                [user_id])

for i in range(1, PRODUCT_COUNT + 1):
    price = random.random()
    user_id = random.randint(1, USER_COUNT)
    unit_id = random.randint(1, 3)
    department_id = random.randint(1, 11)
    db.execute("""INSERT INTO products
                (name, price, user_id, unit_id, department_id) 
                VALUES (?, ?, ?, ?, ?)""",
                ["product" + str(i), price, user_id, unit_id, department_id])
for i in range(1, USER_COUNT + 1):
    shopping_list_id = i
    for j in range(random.randint(0,MAX_ITEMS_SHOPPING_LIST)):
        product_id = random.randint(1, PRODUCT_COUNT)
        amount = random.randint(1, MAX_ITEM_AMOUNT)
        db.execute("""INSERT INTO shopping_list_items
                    (shopping_list_id, product_id, amount)
                    VALUES (?, ?, ?)""",
                    [shopping_list_id, product_id, amount])

for i in range(1, RATING_COUNT + 1):
    user_id = random.randint(1, USER_COUNT)
    product_id = random.randint(1, PRODUCT_COUNT)
    rating = random.randint(1,5)
    db.execute("""INSERT INTO product_ratings
                (product_id, user_id, rating)
                VALUES (?, ?, ?)""",
                [product_id, user_id, rating])

db.commit()
db.close()
