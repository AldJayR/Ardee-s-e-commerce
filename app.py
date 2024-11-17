from flask import Flask, render_template, request, jsonify, session, flash, redirect
from flask_session import Session
from cs50 import SQL
import os
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Mail, Message
import secrets
import datetime

from helpers import login_required, get_base_url

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(16))

# Configure email verification

app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = "ardeesph@gmail.com"
app.config['MAIL_PASSWORD'] = "pcls ysaf sndq zyxs"
app.config['MAIL_DEFAULT_SENDER'] = "ardeesph@gmail.com"
mail = Mail(app)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Initialize the database connection
db = SQL("sqlite:///restaurant.db")


@app.route("/")
def index():
    foods = db.execute("SELECT * FROM menu")
    return render_template("index.html", foods=foods)


@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    if request.method == "POST":
        item_id = request.form.get("food_id")
        menu = db.execute("SELECT * FROM menu WHERE ItemID = ?", item_id)

        name = menu[0]["Name"]
        price = menu[0]["Price"]
        image_url = menu[0]["ImageURL"]

        existing_item = db.execute(
            "SELECT * FROM shopping_cart WHERE item_id = ? AND user_id = ?", item_id, session["user_id"])

        quantity = 1
        total_price = price * quantity

        if existing_item:
            quantity += existing_item[0]["quantity"]
            total_price = price * quantity
            db.execute("UPDATE shopping_cart SET quantity = ?, total_price = ? WHERE item_id = ? AND user_id = ?",
                       quantity, total_price, item_id, session["user_id"])
        else:
            db.execute("INSERT INTO shopping_cart (item_id, user_id, name, price, quantity, total_price, image_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       item_id, session["user_id"], name, price, quantity, total_price, image_url)

        db.execute("INSERT INTO checkout (user_id, item_id, quantity, total_price) VALUES (?, ?, ?, ?)",
                   session["user_id"], item_id, quantity, total_price)

        flash("Item added successfully!", "success")

        return redirect("/cart")

    else:
        shopping_cart = db.execute(
            "SELECT * FROM shopping_cart WHERE user_id = ?", session["user_id"])

        subtotal = sum(item["price"] * item["quantity"] for item in shopping_cart)
        total_items = sum(item["quantity"] for item in shopping_cart)
        return render_template("cart.html", cart=shopping_cart, subtotal=subtotal, total_items=total_items)


@app.route("/cart/info")
@login_required
def cart_info():
    shopping_cart = db.execute("SELECT * FROM shopping_cart WHERE user_id = ?", session["user_id"])
    subtotal = sum(item["price"] * item["quantity"] for item in shopping_cart)
    total_items = sum(item["quantity"] for item in shopping_cart)
    return jsonify({"subtotal": subtotal, "totalItems": total_items})


@app.route("/update_quantity/<int:item_id>", methods=["POST"])
@login_required
def update_quantity(item_id):
    change = request.json.get("change")
    if change is None:
        return jsonify({"error": "Invalid input"}), 400

    current_quantity = db.execute(
        "SELECT quantity FROM shopping_cart WHERE item_id = ? AND user_id = ?", item_id, session["user_id"])[0]["quantity"]

    new_quantity = current_quantity + change

    if new_quantity < 1:
        new_quantity = 1

    # Update quantity in the database
    db.execute("UPDATE shopping_cart SET quantity = ? WHERE item_id = ? AND user_id = ?",
               new_quantity, item_id, session["user_id"])

    return jsonify({"quantity": new_quantity})


@app.route("/delete_item/<int:item_id>", methods=["POST"])
@login_required
def delete_item(item_id):
    db.execute("DELETE FROM shopping_cart WHERE item_id = ? AND user_id = ?",
               item_id, session["user_id"])
    return jsonify({"success": True})


@app.route("/login", methods=["GET", "POST"])
def login():

    if "user_id" in session:
        return redirect("/")

    session.clear()

    if request.method == "GET":
        return render_template("login.html")
    else:

        if not request.form.get("username"):
            flash("Please provide a username", "danger")
            return redirect("/login")
        elif not request.form.get("password"):
            flash("Please provide a password", "danger")
            return redirect("/login")

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(
            rows[0]["hashed_password"], request.form.get("password")
        ):
            flash("Invalid username and/or password", "danger")
            return redirect("/login")

        session["user_id"] = rows[0]["id"]

        return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        if not name:
            flash("Please provide a username", "danger")
        elif not password:
            flash("Please provide a password", "danger")
        elif password != request.form.get("confirmation"):
            flash("Passwords do not match", "danger")
            return redirect("/register")
        elif not email:
            flash("Please provide an email", "danger")
            return redirect("/register")

        existing_user = db.execute("SELECT * FROM users WHERE username = ?", name)

        if existing_user:
            flash("Username already taken", "danger")
            return redirect("/register")

        existing_email = db.execute("SELECT * FROM users WHERE email = ?", email)

        if existing_email:
            flash("Email already taken", "danger")
            return redirect("/register")

        hash = generate_password_hash(password)

        token = secrets.token_hex(16)

        db.execute("INSERT INTO users (username, hashed_password, email, email_token, token_timestamp) VALUES (?, ?, ?, ?, ?)",
                   name, hash, email, token, datetime.datetime.now())

        base_url = get_base_url()

        msg = Message('Confirm Your Email', recipients=[email])
        msg.body = f"Click the following link to verify your email: {
            base_url}/verify_email?token={token}"
        mail.send(msg)

        flash("Please check your email to verify your account", "success")

        return redirect("/")


@app.route("/verify_email")
def verify_email():
    token = request.args.get("token")
    if not token:
        flash("Invalid verification link", "danger")
        return redirect("/")

    user = db.execute("SELECT * FROM users WHERE email_token = ?", token)

    if not user:
        flash("Invalid verification link", "danger")
        return redirect("/")

    token_timestamp = datetime.datetime.strptime(user[0]["token_timestamp"], "%Y-%m-%d %H:%M:%S")
    if datetime.datetime.now() - token_timestamp > datetime.timedelta(days=1):
        flash("Verification link has expired", "danger")
        return redirect("/")

    db.execute("UPDATE users SET email_verified = 1 WHERE id = ?", user[0]["id"])

    flash("Email verified successfully", "success")

    session["user_id"] = user[0]["id"]

    return redirect("/")


@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        subtotal = request.form.get("checkout-subtotal")
        total_items = request.form.get("checkout-total-item")

        if int(total_items) == 0:
            flash("Please order an item before checking out", "warning")
            return redirect("/cart")

    return render_template("checkout.html")


@app.route("/ordered", methods=["GET", "POST"])
def ordered():
    if request.method == "POST":

        full_name = request.form.get("fullName")
        email = request.form.get("email")
        address = request.form.get("address")

        print(full_name)
        print(email)
        print(address)

        if not full_name or not email or not address:
            flash("Please input the required fields", "danger")
            return redirect("/checkout")

        db.execute("DELETE FROM shopping_cart WHERE user_id = ?", session["user_id"])

        flash("Your order is on the way!", "success")
    return redirect("/")
