import os
import time
import re
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def extract(meeting):

    data = {}

    try:
        time = re.findall("[\s\W](\d\d?)[\.\:](\d\d)", meeting)[0]
        if len(time[0]) == 1:
            data["time"] = "0" + str(time[0]) + ":" + str(time[1])
        else:
            data["time"] = str(time[0]) + ":" + str(time[1])
    except:
        pass

    try:
        datelist = re.findall("Date\W*\s*(\d\d?)|Time:\s\w+\s(\d\d)|Date:\s?\w*\s?(\d\d?)|[a-z]\s(\d\d?)[\/][^\:\.]", meeting)[0]
        for element in datelist:
            if element == "":
                continue
            data["date"] = int(element)
            break
    except:
        pass

    try:
        data["subject"] = re.findall("(\w+) Class", meeting, re.IGNORECASE)[0]
    except:
        try:
            data["subject"] = re.findall("Subject\s?\W?\s(\w*)\s?", meeting)[0]
        except:
            try:
                data["subject"] = re.findall("7[Bb]\s([\w\.]*)\s?", meeting)[0]
            except:
                pass

    try:
        data["link"] = re.findall("(https:\/\/[us].*)\s\n", meeting)[0]

        #Works because if zoom link isn't found,
        #the return object of re.findall is None, hence the end indexing [0] throws an error

        data["type"] = "zoom"

        data["id"] = re.findall("(\d{3}\s\d{3}\d?\s\d{3}\d?)", meeting)[0]
        data["teacher"] = re.findall("(.*)\sis inviting", meeting)[0]
        data["password"] = re.findall("Passcode:\s?(.*)\s?\n?", meeting)[0]

    except:
        try:
            link = re.findall("(meet\.google.*\/.*)\s?", meeting)[0].strip()
            data["link"] = "https://" + link
            data["type"] = "gmeet"
            data["code"] = re.findall("meet\.google.*\/(.*)\s?", meeting)[0]
        except:
            print("Skipping invite, no link found")

    return data

def get_day():
    """Gets day value, added here for non repetition"""
    day = int(time.strftime("%d"))

    if day < 7:
        day = day + 7

    day = day % 7

    return day
