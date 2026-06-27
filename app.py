import secrets
import re
import time

from flask import Flask
from flask import abort, flash, redirect, render_template, request, session, g

import config
import products
import users
import units
import departments
import shopping_lists
import shopping_list_items
import product_ratings


app = Flask(__name__)
app.secret_key = config.SECRET_KEY

def require_login():
    if "user_id" not in session:
        abort(403)

def validate_price(price):
    price_regex = r"^(0|[1-9]\d*)([,\.]\d{1,2})?"
    if not re.match(price_regex, price):
        abort(403)
    if len(price) > 8:
        abort(403)

def validate_name(name):
    if len(name) > 50 or not name:
        abort(403)

def validate_username(username):
    errors = []
    if not users.check_availability(username):
        errors.append("VIRHE:  käyttäjätunnus on jo käytössä")
    if len(username) < 5:
        errors.append("""VIRHE:  käyttäjätunnus on liian lyhyt.
                        Käyttäjätunnuksen tulee olla vähintään 5 merkkiä.""")
    if len(username) > 30:
        errors.append("""VIRHE:  käyttäjätunnus on liian pitkä.
                        Käyttäjätunnuksen tulee olla enintään 30 merkkiä.""")
    pattern = r'^[\w-]+'
    if not re.match(pattern, username):
        errors.append("""VIRHE:  käyttäjätunnus saa sisältää vain kirjaimia,
                        numeroita, alaviivoja (_) tai yhdysviivoja (-).""")
    if errors:
        for error in errors:
            flash(error, category="error")
        return False
    return True

def validate_passwords(password1, password2):
    errors = []
    if password1 != password2:
        errors.append("VIRHE: salasanat eivät ole samat")
    if len(password1) < 8:
        errors.append("""VIRHE: Salasana on liian lyhyt.
                        Salasanan pituuden tulee olla vähintään 8 merkkiä.""")
    if password1.isalpha():
        errors.append("VIRHE: Salasanan tulee sisältää numeroita tai erikoismerkkejä.")
    if errors:
        for error in errors:
            flash(error, category="error")
        return False
    return True

def validate_unit(unit):
    all_units = [unit["name"] for unit in units.get_all_units()]
    if unit not in all_units:
        abort(403)

def validate_department(department):
    all_departments = [department["name"] for department in departments.get_all_departments()]
    if department not in all_departments:
        abort(403)

def validate_rating(rating):
    ratings = [str(number) for number in range(1,6)]
    if rating not in ratings:
        abort(403)

def validate_amount(amount):
    amount_regex = r"^(0|[1-9]\d*)([,\.]\d{1,2})?"
    if not re.match(amount_regex, amount):
        abort(403)
    if len(amount) > 8:
        abort(403)

def format_amount(amount):
    string = str(amount)
    return string.replace(",",".")

def current_shopping_list():
    shopping_list = None
    if "shopping_list_id" in session:
        shopping_list_id = session["shopping_list_id"]
        shopping_list = shopping_list_items.get_items(shopping_list_id)
    return shopping_list

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

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
    return render_template("find_product.html",query=query,
                            results=results, shopping_list=shopping_list)

@app.route("/product/<int:product_id>")
def show_product(product_id):
    if session:
        user_id = session["user_id"]
        product = products.get_product(product_id,user_id)
    else:
        product = products.get_product(product_id)
    if not product:
        abort(404)
    shopping_list = current_shopping_list()
    return render_template("show_product.html", product=product, shopping_list=shopping_list)

@app.route("/rate_product", methods= ["POST"])
def rate_product():
    require_login()
    user_id = session["user_id"]
    check_csrf()
    product_id = request.form["product_id"]
    product = products.get_product(product_id)
    if not product:
        abort(404)
    rating = request.form["rating"]
    validate_rating(rating)
    rating = int(rating)
    product_ratings.rate(product_id, user_id, rating)
    return redirect(request.referrer)


@app.route("/adjust_amount", methods= ["POST"])
def adjust_amount():
    require_login()
    check_csrf()
    product_id = request.form["product_id"]
    product = products.get_product(product_id)
    if not product:
        abort(404)
    amount = request.form["amount"]
    if amount:
        validate_amount(amount)
        amount = format_amount(amount)
    else:
        amount = 1
    shopping_list_id = session["shopping_list_id"]
    adjust = request.form.get("adjust")
    if adjust == "-":
        shopping_list_items.substract(amount, product_id, shopping_list_id)
    elif adjust == "+":
        shopping_list_items.add(amount, product_id, shopping_list_id)
    return redirect(request.referrer)

@app.route("/new_product")
def new_product():
    require_login()
    all_units = units.get_all_units()
    all_departments= departments.get_all_departments()
    shopping_list = current_shopping_list()
    return render_template("new_product.html", units=all_units,
                            departments=all_departments, shopping_list=shopping_list)

@app.route("/create_product", methods=["POST"])
def create_product():
    require_login()
    check_csrf()
    user_id = session["user_id"]
    name = request.form["name"]
    validate_name(name)
    name = name.capitalize()
    price = request.form["price"]
    if not price:
        price = 0
    validate_price(price)
    unit = request.form["unit"]
    validate_unit(unit)
    unit_id = units.get_unit_id(unit)
    department = request.form["department"]
    if not department:
        department = "other"
    validate_department(department)
    department_id = departments.get_department_id(department)
    product_id = products.add_product(name, price, user_id, unit_id, department_id)
    rating = request.form["rating"]
    if rating:
        product_ratings.rate(product_id, user_id, rating)
    flash("Tuote luotu", category="success")
    return redirect("/")

@app.route("/edit_product/<int:product_id>")
def edit_product(product_id):
    require_login()
    user_id = session["user_id"]
    product = products.get_product(product_id, user_id)
    if not product:
        abort(404)
    if product["user_id"] != session["user_id"]:
        abort(403)
    all_units = units.get_all_units()
    all_departments= departments.get_all_departments()
    shopping_list = current_shopping_list()
    return render_template("edit_product.html", product=product,
                            units=all_units, departments=all_departments,
                            shopping_list=shopping_list)

@app.route("/update_product", methods=["POST"])
def update_product():
    require_login()
    check_csrf()
    user_id = session["user_id"]
    product_id = request.form["product_id"]
    product = products.get_product(product_id)
    if not product:
        abort(404)
    if product["user_id"] != user_id:
        abort(403)
    name = request.form["name"]
    validate_name(name)
    name = name.capitalize()
    price = request.form["price"]
    if not price:
        price = 0
    validate_price(price)
    unit = request.form["unit"]
    validate_unit(unit)
    unit_id = units.get_unit_id(unit)
    department = request.form["department"]
    validate_department(department)
    department_id = departments.get_department_id(department)
    products.update_product(product_id, name, price, unit_id, department_id)
    rating = request.form["rating"]
    if rating:
        product_ratings.rate(product_id, user_id, rating)
    flash("Tuote päivitetty", category="success")
    return redirect("/product/" +str(product_id))

@app.route("/remove_product/<int:product_id>", methods=["GET", "POST"])
def remove_product(product_id):
    require_login()
    product = products.get_product(product_id)
    if not product:
        flash("Tuotetta ei löydy")
        return redirect("/")
    if product["user_id"] != session["user_id"]:
        abort(403)
    if request.method == "GET":
        shopping_list = current_shopping_list()
        return render_template("remove_product.html", product=product, shopping_list=shopping_list)
    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            products.remove_product(product_id)
            return redirect("/")
    return redirect("/product/" + str(product_id))

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    shopping_list_id = shopping_lists.get_id(user_id)
    user_shopping_list = shopping_list_items.get_items(shopping_list_id)
    total_price = shopping_list_items.total_price(shopping_list_id)
    shopping_list = current_shopping_list()
    return render_template("show_user.html", user=user,
                            user_shopping_list=user_shopping_list,
                            shopping_list=shopping_list,
                            total_price=total_price)

@app.route("/register")
def register():
    shopping_list = current_shopping_list()
    return render_template("register.html", shopping_list=shopping_list)

@app.route("/create_user", methods=["POST"])
def create_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if not validate_username(username) or not validate_passwords(password1, password2):
        return redirect("/register")
    users.create_user(username,password1)
    flash(f"Käyttäjätunnus {username} luotu onnistuneesti", category="success")
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        next_page = request.referrer
        if "/register" in next_page:
            next_page = "/"
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        next_page = request.form["next_page"]
        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            shopping_list_id = shopping_lists.get_id(user_id)
            if not shopping_list_id:
                shopping_lists.add("Oma Kauppalista", user_id)
                shopping_list_id = shopping_lists.get_id(user_id)
            session["shopping_list_id"] = shopping_list_id
            return redirect(next_page)
        flash("VIRHE:  väärä tunnus tai salasana", category="error")
    return render_template("login.html", next_page=next_page)

@app.route("/logout")
def logout():
    require_login()
    del session["username"]
    del session["user_id"]
    if "shopping_list_id" in session:
        del session["shopping_list_id"]
    if "csrf_token" in session:
        del session["csrf_token"]
    return redirect("/")

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response
