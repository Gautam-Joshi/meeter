import re

def main():

    text = """[26/08, 12:48] Vaneeta Mam ( Geo,His,Civ ): Pratibha Phy edu. is inviting you to a scheduled Zoom meeting.

Topic: Pratibha Phy edu.'s Personal Meeting Room

Join Zoom Meeting
https://us04web.zoom.us/j/2030800092?pwd=QjFmYjBhWVMxL0cxcy9VVDdGYVNyZz09

Meeting ID: 203 080 0092
Passcode: 1234

Class : 7th all sections
Time : 7:30 am ( Monday, Wednesday, Friday)
[26/08, 12:49] Vaneeta Mam ( Geo,His,Civ ): To join the meeting on Google Meet, click this link:
https://meet.google.com/khn-ywsr-uws

Or open Meet and enter this code: khn-ywsr-uws
*English Class at 8:15am ,on 29/8*
[26/08, 12:49] Vaneeta Mam ( Geo,His,Civ ): Subject: Hindi (1st  Language)
Class : 7 B
Date: August 29, 2021
Time: 9:10 AM India

https://meet.google.com/bgy-asbg-rtf


व्याकरण पुस्तक व CCT नोटबुक के साथ समय पर कक्षा में उपस्थित रहें।
[26/08, 12:49] Vaneeta Mam ( Geo,His,Civ ): To join the meeting on Google Meet, click this link:
https://meet.google.com/nwp-wakm-gca

Or open Meet and enter this code: nwp-wakm-gca

For 7B Science class at 10.10am on 29/08/2021
[26/08, 12:50] Vaneeta Mam ( Geo,His,Civ ): To join the meeting on Google Meet, click this link:
https://meet.google.com/odd-msac-wje

Or open Meet and enter this code: odd-msac-wje
Class 7b
Join for maths   at 11:10 am on 29/ 08/2021
[26/08, 12:50] Vaneeta Mam ( Geo,His,Civ ): https://meet.google.com/hmd-ddzp-qbg
Time- 12:15 pm
Date-29-08-2021
Subject- Geography
[26/08, 14:57] Vaneeta Mam ( Geo,His,Civ ): Simran Dhillon is inviting you to a scheduled Zoom meeting.

Topic: Simran Dhillon's Zoom Meeting
Time: Aug 29, 2021 12:15 PM India

Join Zoom Meeting
https://us04web.zoom.us/j/4290541070?pwd=UEJ3QXd5VGRkRkxVZTF6VkRPa256dz09

Meeting ID: 429 054 1070
Passcode: 4zWiu0
subject- Geography"""
    invites = re.split("\[.*\].*:\s?", text)

    for meeting in invites:

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

        for element in data:
            print(data[element])
        print("\n")

if __name__ == "__main__":
    main()