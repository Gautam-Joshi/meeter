import re
from cs50 import SQL
import time
from helpers import extract

db = SQL("sqlite:///meetings.db")

def main():
    rows = db.execute("SELECT * FROM meetings WHERE user_session IN (?)", "1")
    for entry in rows:
        if entry["teacher"] is not None:
            print(entry["teacher"])

if __name__ == "__main__":
    main()