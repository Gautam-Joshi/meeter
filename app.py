import os

import re
import time

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import extract, login_required, apology, get_day
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

@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Welcome here!"""
    if request.method == "GET":
        return render_template("add.html")

    if request.method == "POST":

        text = request.form.get("message")

        invites = re.split("\[.*\].*:\s?", text)

        for meeting in invites:
            #Split returns first and last strings as ""
            if meeting == "":
                continue

            #Call our regex helper to give a dict for current meeting
            data = extract(meeting)

            #Check if no invite
            try:
                test = data["time"]
                del test
            except:
                continue

            # Check for date presence
            try:
                test = data["date"]
                del test
            except:
                #Set date based on user input
                if request.form.get("date_preference") == "0":
                    data["date"] = int(time.strftime("%d"))
                else:
                    data["date"] = int(time.strftime("%d")) + 1

            #Use % 7 to set unique day id
            if int(data["date"]) < 7:
                data["date"] = int(data["date"]) + 7
            day = int(data["date"]) % 7

            #Find meeting type
            if data["type"] == "zoom":
                #meet type 0 for zoom
                meet_type = 0
            else:
                #meet type 1 for gmeet
                meet_type = 1

            #Maintenence
            #Delete old inactive meetings of same day
            db.execute("DELETE FROM meetings WHERE day IN (?) AND active IN (?)", day, "0")

            #Set meetings of days except today and tomorrow as inactive
            if day == 6:
                day1 = 6
                day2 = 0
            else:
                day1 = day
                day2 = day1 + 1
            db.execute("UPDATE meetings SET active = (?) WHERE day NOT IN (?, ?)", "0", day1, day2)
            del day1
            del day2
            #Maintenence Done

            #Add common data to meetings
            db.execute("INSERT INTO meetings (user_session, link, time, day, type, active) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"], data["link"], data["time"], day, meet_type, "1")
            print("Action: Meeting Added")

            #Get meeting id of currently added meeting to do case based data addition
            meeting = db.execute("SELECT meeting_id FROM meetings WHERE day IN (?) AND user_session IN (?) AND time IN (?) AND link IN (?)", day, session["user_id"], data["time"], data["link"])
            print("Action: Meeting Accessed")

            #Add subject if present
            try:
                db.execute("UPDATE meetings SET subject = (?) WHERE meeting_id = (?)", data["subject"], meeting[0]["meeting_id"])
                print("Action: Subject Added")
            except:
                pass
            #Add teacher if present
            try:
                db.execute("UPDATE meetings SET teacher = (?) WHERE meeting_id = (?)", data["teacher"], meeting[0]["meeting_id"])
                print("Action: Teacher Added")
            except:
                pass

            if meet_type == 0:
                #Add MID and passcode for zoom
                db.execute("UPDATE meetings SET mid = (?), passcode = (?) WHERE meeting_id IN (?)", data["id"], data["password"], meeting[0]["meeting_id"])
                print("Action: MID/Pass - Zoom")
            else:
                #Add meet code for gmeet
                db.execute("UPDATE meetings SET gmeet_code = (?) WHERE meeting_id IN (?)", data["code"], meeting[0]["meeting_id"])
                print("Action: Gmeet Code Added")

            db.execute("UPDATE meetings SET subject = NULL WHERE subject = (?)", "")
            for element in data:
                print(data[element])
            print("\n")

        return redirect("/")

@app.route("/edit", methods=["GET","POST"])
@login_required
def edit():
    
    if request.method=="GET":
        day = get_day()

        my_meetings = db.execute("SELECT * FROM meetings WHERE user_session IN (?) AND day IN (?) AND active IN (?) ORDER BY time", session["user_id"], day, "1")

        return render_template("edit.html", meetings = my_meetings)

    if request.method=="POST":

        day = get_day()

        my_meetings = db.execute("SELECT * FROM meetings WHERE user_session IN (?) AND day IN (?) AND active IN (?)", session["user_id"], day, "1")

        for meeting in my_meetings:

            #Update Time if changed
            if request.form.get("time" + str(meeting["meeting_id"])):
                db.execute("UPDATE meetings SET time = (?) WHERE meeting_id IN (?)", request.form.get("time" + str(meeting["meeting_id"])), meeting["meeting_id"])

            #Update Subject if changed
            if request.form.get("subject" + str(meeting["meeting_id"])):
                db.execute("UPDATE meetings SET subject = (?) WHERE meeting_id IN (?)", request.form.get("subject" + str(meeting["meeting_id"])), meeting["meeting_id"])

            #Update Teacher if changed
            if request.form.get("teacher" + str(meeting["meeting_id"])):
                db.execute("UPDATE meetings SET teacher = (?) WHERE meeting_id IN (?)", request.form.get("teacher" + str(meeting["meeting_id"])), meeting["meeting_id"])

            #Update Link if changed
            if request.form.get("link" + str(meeting["meeting_id"])):
                db.execute("UPDATE meetings SET link = (?) WHERE meeting_id IN (?)", request.form.get("link" + str(meeting["meeting_id"])), meeting["meeting_id"])

            if meeting["type"] == "0":
                #zoom
                
                #Update MID if changed
                if request.form.get("mid" + str(meeting["meeting_id"])):
                    db.execute("UPDATE meetings SET mid = (?) WHERE meeting_id IN (?)", request.form.get("mid" + str(meeting["meeting_id"])), meeting["meeting_id"])

                #Update Passcode if changed
                if request.form.get("passcode" + str(meeting["meeting_id"])):
                    db.execute("UPDATE meetings SET passcode = (?) WHERE meeting_id IN (?)", request.form.get("passcode" + str(meeting["meeting_id"])), meeting["meeting_id"])
            else:
                #gmeet

                #Update gmeet_code if changed
                if request.form.get("gmeet_code" + str(meeting["meeting_id"])):
                    db.execute("UPDATE meetings SET gmeet_code = (?) WHERE meeting_id IN (?)", request.form.get("gmeet_code" + str(meeting["meeting_id"])), meeting["meeting_id"])
        return redirect("/")

@app.route("/")
@login_required
def index():
    day = get_day()

    #If meetings are there
    my_meetings = db.execute("SELECT * FROM meetings WHERE user_session IN (?) AND day IN (?) AND active IN (?) ORDER BY time", session["user_id"], day, "1")

    if len(my_meetings) > 0:
        return render_template("index.html", meetings = my_meetings)

    #If suggested meetings are there
    suggestions = db.execute("SELECT * FROM meetings WHERE user_session IN (?) AND day IN (?) AND active IN (?) ORDER BY time", session["user_id"], day, "0")

    if len(suggestions) > 0:
        return render_template("index.html", suggestions = suggestions)

    return render_template("index.html")

@app.route("/remove")
def remove():

    db.execute("DELETE FROM meetings WHERE meeting_id IN (?)", request.args.get("meeting_id"))

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

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, pwhash)

    return redirect("/login")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
