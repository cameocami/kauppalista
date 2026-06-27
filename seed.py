import random
import sqlite3

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM products")
db.execute("DELETE FROM shopping_lists")
db.execute("DELETE FROM shopping_list_items")
db.execute("DELETE FROM product_ratings")

user_count = 1000
product_count = 10**5
max_items_per_shopping_list = 50
max_item_amount = 10
rating_count = 10**6

'''
initialize users and their shopping lists
'''
for i in range(1, user_count + 1):
    result = db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])
    user_id = result.lastrowid
    db.execute("INSERT INTO shopping_lists (user_id) VALUES (?)", 
                [user_id])

'''
initialize products
'''

for i in range(1, product_count + 1):
    price = random.random()
    user_id = random.randint(1, user_count)
    unit_id = random.randint(1, 3)
    department_id = random.randint(1, 11)
    db.execute("""INSERT INTO products
                (name, price, user_id, unit_id, department_id) 
                VALUES (?, ?, ?, ?, ?)""",
                ["product" + str(i), price, user_id, unit_id, department_id])

'''
add products to each shopping list with random amount 1-10
'''

for i in range(1, user_count + 1):
    shopping_list_id = i
    for j in range(random.randint(0,max_items_per_shopping_list)):
        product_id = random.randint(1, product_count)
        amount = random.randint(1, max_item_amount)
        db.execute("""INSERT INTO shopping_list_items
                    (shopping_list_id, product_id, amount)
                    VALUES (?, ?, ?)""",
                    [shopping_list_id, product_id, amount])

'''
create product ratings
'''

for i in range(1, rating_count + 1):
    user_id = random.randint(1, user_count)
    product_id = random.randint(1, product_count)
    rating = random.randint(1,5)
    db.execute("""INSERT INTO product_ratings
                (product_id, user_id, rating)
                VALUES (?, ?, ?)""",
                [product_id, user_id, rating])

db.commit()
db.close()
