from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import products, users, units, departments
import re

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def validate_price(price):
    price_regex = r'(^\d+(\,\d{1,2})?$)'
    if not re.match(price_regex, price):
        abort(403)
    if len(price) > 8:
        abort(403)

def validate_name(name):
    if len(name) > 50 or not name:
        abort(403)

@app.route("/")
def index():
    all_products = products.get_products()
    return render_template("index.html", products=all_products)

@app.route("/find_product")
def find_product():
    query = request.args.get("query")
    if query:
        results = products.find_products(query)
    else:
        query = ""
        results = []
    return render_template("find_product.html", query=query, results=results)

@app.route("/product/<int:product_id>")
def show_product(product_id):
    product = products.get_product(product_id)
    if not product:
        abort(404)
    return render_template("show_product.html", product=product)

@app.route("/new_product")
def new_product():
    require_login()
    all_units = units.get_all_units()
    all_departments= departments.get_all_departments()
    return render_template("new_product.html", units=all_units, departments=all_departments)

@app.route("/create_product", methods=["POST"])
def create_product():
    require_login()
    name = request.form["name"]
    validate_name(name)
    price = request.form["price"]
    validate_price(price)
    user_id = session["user_id"]
    unit = request.form["unit"]
    unit_id = units.get_unit_id(unit)
    department = request.form["department"]
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
    return render_template("edit_product.html", product=product,  units=all_units, departments=all_departments)

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
    unit_id = units.get_unit_id(unit)
    department = request.form["department"]
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
        return render_template("remove_product.html", product=product)
    if request.method == "POST":
        if "remove" in request.form:
            products.remove_product(product_id)
            return redirect("/")
        else:
            return redirect("/product/" + str(product_id))

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    products = users.get_products(user_id)
    return render_template("show_user.html", user=user, products=products)

@app.route("/register")
def register():
    return render_template("register.html")

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
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    require_login()
    del session["username"]
    del session["user_id"]
    return redirect("/")