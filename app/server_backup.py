from flask import Flask, request, redirect, session, send_from_directory
import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash

from charts.chart_api import chart_api
from trading.trading_api import trading_api
from trading.trading_db import create_trading_tables


app = Flask(__name__)
app.secret_key = "change-this-secret"


# =========================
# AUTH MIDDLEWARE
# =========================

PUBLIC_PATHS = {
    "/",
    "/login",
    "/register",
}


@app.before_request
def require_login():

    path = request.path

    # דפים שלא דורשים התחברות
    if path in PUBLIC_PATHS:
        return

    # קבצים סטטיים
    if path.startswith("/static/"):
        return

    if path.startswith("/charts/static/"):
        return

    # API מחזיר JSON במקום redirect
    if "username" not in session:

        if path.startswith("/api/"):
            return {
                "error": "Unauthorized"
            }, 401

        return redirect("/login")


# =========================
# DATABASE
# =========================

def db():
    return sqlite3.connect("users.db")


with db() as conn:
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )
    """)


# =========================
# INIT DATABASES
# =========================

create_trading_tables()


# =========================
# BLUEPRINTS
# =========================

app.register_blueprint(chart_api)
app.register_blueprint(trading_api)


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return redirect("/login")


# =========================
# LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        with db() as conn:

            user = conn.execute(
                """
                SELECT *
                FROM users
                WHERE username=?
                """,
                (username,)
            ).fetchone()


        if user and check_password_hash(user[2], password):

            session["username"] = username

            return redirect("/dashboard")


        return "Wrong username or password"


    return send_from_directory(
        "/app/public",
        "index.html"
    )


# =========================
# REGISTER
# =========================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        hashed = generate_password_hash(password)

        try:

            with db() as conn:

                conn.execute(
                    """
                    INSERT INTO users(username,password)
                    VALUES (?,?)
                    """,
                    (
                        username,
                        hashed
                    )
                )


            from trading.trading_db import create_account

            create_account(username)


            return redirect("/login")


        except sqlite3.IntegrityError:

            return "Username already exists"


    return send_from_directory(
        "/app/public",
        "register.html"
    )


# =========================
# DASHBOARD
# =========================

@app.route("/dashboard")
def dashboard():

    with open(
        "/app/public/dashboard.html",
        "r",
        encoding="utf-8"
    ) as file:

        html = file.read()


    html = html.replace(
        "{{username}}",
        session["username"]
    )


    return html


# =========================
# CHART STATIC
# =========================

@app.route("/charts/static/<path:filename>")
def chart_files(filename):

    return send_from_directory(
        "/app/charts",
        filename
    )


# =========================
# CHART PAGE
# =========================

@app.route("/charts/<symbol>")
def charts(symbol):

    with open(
        "/app/charts/chart.html",
        "r",
        encoding="utf-8"
    ) as file:

        html = file.read()


    return html.replace(
        "AAPL",
        symbol
    )


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# =========================
# START
# =========================

app.run(
    host="0.0.0.0",
    port=5000
)
