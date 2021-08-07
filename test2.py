import re

def main():

    text = """[7/27, 19:19] A Joshi: Pratibha Phy edu. is inviting you to a scheduled Zoom meeting.

Topic: Pratibha Phy edu.'s Personal Meeting Room

Join Zoom Meeting
https://us04web.zoom.us/j/2030800092?pwd=QjFmYjBhWVMxL0cxcy9VVDdGYVNyZz09

Meeting ID: 203 080 0092
Passcode: 1234
Class : 7th Physical education
Time : 7:30 AM
[7/27, 19:19] A Joshi: To join the meeting on Google Meet, click this link:
https://meet.google.com/vsi-cuff-mxg
 7B History class
*Time-7.55am*
Date- 28-7-21
[7/27, 19:19] A Joshi: To join the meeting on Google Meet, click this link:
https://meet.google.com/vsi-cuff-mxg
 7B G.K Class
Time- 11.10am
Date- 28-7-21
[7/27, 19:19] A Joshi: To join the meeting on Google Meet, click this link:
https://meet.google.com/nwp-wakm-gca

Or open Meet and enter this code: nwp-wakm-gca

For 7B Science class at 10.10am on 28/07/2021
[7/27, 19:19] A Joshi: Saitah Badhawan is inviting you to a scheduled Zoom meeting.

Topic: Saitah Badhawan's Zoom Meeting
Time: Jul 28, 2021 09:10 AM Mumbai, Kolkata, New Delhi

Join Zoom Meeting
https://us04web.zoom.us/j/78711714157?pwd=WjUzSkRyWjBpSDJJRHFhcUdIYiszQT09

Meeting ID: 787 1171 4157
Passcode: 8WCMrV

Class 7b maths
[7/27, 19:19] A Joshi: gurinder kaur is inviting you to a scheduled Zoom meeting.

Topic: gurinder kaur's Personal Meeting Room

Join Zoom Meeting
https://us04web.zoom.us/j/9582412379?pwd=RFdtUjZ5SFZGMnBlajA0Vzd5bDFtdz09

Meeting ID: 958 241 2379
Passcode: Punjabi

Join Punjabi clasd tomorrow at 12.15"""
    invites = re.split("\[.*\].*\n", text)
    for meeting in invites:
        if meeting == "":
            continue

        data = {}
        #findall return a list of match groups list->[match groups -> (a,b)]
        try:
            datelist = re.findall("Date\W*\s*(\d\d?)|Time:\s\w+\s(\d\d)|Date:\s?\w*\s?(\d\d?)|[a-z]\s(\d\d?)[\/][^\:\.]", meeting)[0]
            for element in datelist:
                if element == "":
                    continue
                data["date"] = int(element)
                break
        except:
            pass

        for element in data:
            print(data[element])

if __name__ == "__main__":
    main()