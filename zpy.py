import re

def main():
    months = ["Ja", "Fe", "Mar","Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    for num, month in enumerate(months):
        if re.search(month, "jul 07, 007", re.IGNORECASE):
            print ("Found using re! " + str (num + 1))

if __name__ == "__main__":
    main()