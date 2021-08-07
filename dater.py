import re

def main():
    datea = {}

    # pattern says (maybe a word, maybe space (if word), a digit, a maybe second digit, then a break or a space)
    datea["datf1"] = re.split("\w*?\s?(\d\d?)\W?\s?","28-7-21")
    datea["datf3"] = re.split("\w*?\s?(\d\d?)\W?\s?","25/7")
    datea["datf4"] = re.split("\w*?\s?(\d\d?)\W?\s?","2.08.2021")
    datea["datf5"] = re.split("\w*?\s?(\d\d?)\W?\s?","August 03 ,2021")
    datea["datf2"] = re.split("\w*?\s?(\d\d?)\W?\s?","Jul 28, 2021")
    datea["tf1"] = re.split("(\d\d?)\W(\d\d)","7:30 AM")
    datea["tf2"] = re.split("(\d\d?)\W(\d\d)","7.55am")
    datea["tf3"] = re.split("(\d\d?)\W(\d\d)","12.15")

    for entry in datea:
        print(datea[entry])

if __name__ == "__main__":
    main()