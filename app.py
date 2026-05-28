import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config
import products

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_products = products.get_products()
    return render_template("index.html", products=all_products)

@app.route("/product/<int:product_id>")
def show_product(product_id):
    product = products.get_product(product_id)
    return render_template("show_product.html", product=product)

@app.route("/new_product")
def new_product():
    return render_template("new_product.html")

@app.route("/create_product", methods=["POST"])
def create_product():
    name = request.form["name"]
    price = request.form["price"]
    user_id = session["user_id"]

    products.add_product(name, price, user_id)

    return redirect("/")

@app.route("/edit_product/<int:product_id>")
def edit_product(product_id):
    product = products.get_product(product_id)
    return render_template("edit_product.html", product=product)

@app.route("/update_product", methods=["POST"])
def update_product():
    product_id = request.form["product_id"]
    name = request.form["name"]
    price = request.form["price"]

    products.update_product(product_id, name, price)

    return redirect("/product/" +str(product_id))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql,[username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]
        
        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")