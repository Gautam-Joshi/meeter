import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import extract, login_required, apology
from math import modf

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///meetings.db")

#!comes after @login_required

@app.route("/", methods=["GET", "POST"])
def index():
    """Welcome here!"""
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":

        text = str(request.form.get("message"))
        print(text)

        invites = re.split("\[.*\].*\n", text)

        for meeting in invites:
            if meeting == "":
                continue

            data = extract(meeting)

            for element in data:
                print(data[element])
            print("\n")

        return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form.get("username")

        if not username:
            return apology("Must enter Username")

        match = db.execute("SELECT username FROM users WHERE username=(?)", username)
        if match:
            return apology("Username already exists!")

        password = request.form.get("password")

        if not password:
            return apology("Must enter Password")

        passwordconfirm = request.form.get("confirmation")

        if password != passwordconfirm:
            return apology("Enter Matching Passwords!")

        pwhash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        db.execute("INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)", username, pwhash, "10000")

    return redirect("/login")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)