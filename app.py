from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import products, users, units, departments, shopping_lists, shopping_list_items
import re

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def validate_price(price):
    price_regex = r'^(0|[1-9]\d*)([,\.]\d{1,2})?'
    if not re.match(price_regex, price):
        abort(403)
    if len(price) > 8:
        abort(403)

def validate_name(name):
    if len(name) > 50 or not name:
        abort(403)

def validate_unit(unit):
    all_units = [unit["name"] for unit in units.get_all_units()]
    if unit not in all_units:
        abort(403)

def validate_department(department):
    all_departments = [department["name"] for department in departments.get_all_departments()]
    if department not in all_departments:
        abort(403)

def validate_amount(amount):
    amount_regex = r'^(0|[1-9]\d*)([,\.]\d{1,2})?'
    if not re.match(amount_regex, amount):
        abort(403)
    if len(amount) > 8:
        abort(403)

def current_shopping_list():
    shopping_list_id = session["shopping_list_id"]
    shopping_list = shopping_list_items.get_items(shopping_list_id)
    return shopping_list

@app.route("/")
def index():
    all_products = products.get_products()
    shopping_list = current_shopping_list()
    return render_template("index.html", products=all_products, shopping_list=shopping_list)

@app.route("/find_product")
def find_product():
    query = request.args.get("query")
    if query:
        results = products.find_products(query)
    else:
        query = ""
        results = []
    shopping_list = current_shopping_list()
    return render_template("find_product.html", query=query, results=results, shopping_list=shopping_list)

@app.route("/product/<int:product_id>")
def show_product(product_id):
    product = products.get_product(product_id)
    if not product:
        abort(404)
    shopping_list = current_shopping_list()
    return render_template("show_product.html", product=product, shopping_list=shopping_list)

@app.route("/add_item/<int:product_id>", methods= ["POST"])
def add_item(product_id):
    require_login()
    product = products.get_product(product_id)
    if not product:
        abort(404)
    added_amount = request.form["amount"]
    validate_amount(added_amount)
    added_amount = float(added_amount)
    shopping_list_id = session["shopping_list_id"]
    if shopping_list_items.is_on_list(product_id, shopping_list_id):
        existing_amount = shopping_list_items.amount(product_id, shopping_list_id)
        shopping_list_items.update_amount(existing_amount + added_amount, shopping_list_id, product_id)
    else:
        shopping_list_items.add_new(shopping_list_id, product_id, added_amount)
    shopping_list = current_shopping_list()
    return render_template("show_product.html", product=product, shopping_list=shopping_list)

@app.route("/new_product")
def new_product():
    require_login()
    all_units = units.get_all_units()
    all_departments= departments.get_all_departments()
    shopping_list = current_shopping_list()
    return render_template("new_product.html", units=all_units, departments=all_departments, shopping_list=shopping_list)

@app.route("/create_product", methods=["POST"])
def create_product():
    require_login()
    name = request.form["name"]
    validate_name(name)
    price = request.form["price"]
    validate_price(price)
    user_id = session["user_id"]
    unit = request.form["unit"]
    validate_unit(unit)
    unit_id = units.get_unit_id(unit)
    department = request.form["department"]
    validate_department(department)
    department_id = departments.get_department_id(department)
    products.add_product(name, price, user_id, unit_id, department_id)
    return redirect("/")

@app.route("/edit_product/<int:product_id>")
def edit_product(product_id):
    require_login()
    product = products.get_product(product_id)
    if not product:
        abort(404)
    if product["user_id"] != session["user_id"]:
        abort(403)
    all_units = units.get_all_units()
    all_departments= departments.get_all_departments()
    shopping_list = current_shopping_list()
    return render_template("edit_product.html", product=product,  units=all_units, departments=all_departments, shopping_list=shopping_list)

@app.route("/update_product", methods=["POST"])
def update_product():
    require_login()
    product_id = request.form["product_id"]
    product = products.get_product(product_id)
    if not product:
        abort(404)
    if product["user_id"] != session["user_id"]:
        abort(403)
    name = request.form["name"]
    validate_name(name)
    price = request.form["price"]
    validate_price(price)
    unit = request.form["unit"]
    validate_unit(unit)
    unit_id = units.get_unit_id(unit)
    department = request.form["department"]
    validate_department(department)
    department_id = departments.get_department_id(department)
    products.update_product(product_id, name, price, unit_id, department_id)
    return redirect("/product/" +str(product_id))

@app.route("/remove_product/<int:product_id>", methods=["GET", "POST"])
def remove_product(product_id):
    require_login()
    product = products.get_product(product_id)
    if not product:
        abort(404)
    if product["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        shopping_list = current_shopping_list()
        return render_template("remove_product.html", product=product, shopping_list=shopping_list)
    if request.method == "POST":
        if "remove" in request.form:
            shopping_list_items.remove_product_from_all(product_id)
            products.remove_product(product_id)
            return redirect("/")
        else:
            return redirect("/product/" + str(product_id))

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    shopping_list_id = shopping_lists.get_id(user_id)
    user_shopping_list = shopping_list_items.get_items(shopping_list_id)
    shopping_list = current_shopping_list()
    return render_template("show_user.html", user=user, user_shopping_list=user_shopping_list, shopping_list=shopping_list)

@app.route("/register")
def register():
    shopping_list = current_shopping_list()
    return render_template("register.html", shopping_list=shopping_list)

@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    if not users.check_availability(username):
        return "VIRHE: käyttäjätunnus on jo käytössä"
    users.create_user(username,password1)
    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        shopping_list = current_shopping_list()
        return render_template("login.html", shopping_list=shopping_list)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            shopping_list_id = shopping_lists.get_id(user_id)
            if not shopping_list_id:
                shopping_lists.add("Default", user_id)
                shopping_list_id = shopping_lists.get_id(user_id)
            session["shopping_list_id"] = shopping_list_id
            return redirect("/")
        return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    require_login()
    del session["username"]
    del session["user_id"]
    del session["shopping_list_id"]
    return redirect("/")


