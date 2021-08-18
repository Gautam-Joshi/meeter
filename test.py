import re

def main():

    text = """[7:48 AM, 8/7/2021] A Joshi: Class 7B
Music

Time 9.10AM


Rammi Kaur is inviting you to a scheduled Zoom meeting.

Join Zoom Meeting
https://us04web.zoom.us/j/71519663328?pwd=Yk9iUWhyYXFIQTdLRnJEb1FGMi9nUT09

Meeting ID: 715 1966 3328
Passcode: S6Vmge"""
    invites = re.split("\[.*\]\s?\w+\s?\w+\s?\W\s", text)

    for meeting in invites:

        data = {}

        if meeting == "":
            continue

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
                pass
            

        try:
            data["link"] = re.findall("(https:\/\/[us].*)\s\n", meeting)[0]

            #Works because if zoom link isn't found,
            #the return object of re.findall is None, hence the end indexing [0] throws an error

            data["type"] = "zoom"

            data["id"] = re.findall("(\d{3}\s\d{3}\d?\s\d{3}\d?)", meeting)[0]
            data["teacher"] = re.findall("(\w+\s\w+)\sis inviting", meeting)[0]
            data["password"] = re.findall("Passcode:\s?(.*)\s?\n?", meeting)[0]

        except:
            try:
                link = re.findall("(meet\.google.*\/.*)\s?", meeting)[0].strip()
                data["link"] = "https://" + link
                data["type"] = "gmeet"
                data["code"] = re.findall("meet\.google.*\/(.*)\s?", meeting)[0]
            except:
                print("Skipping invite, no link found")

        for element in data:
            print(data[element])
        print("\n")

if __name__ == "__main__":
    main()