#!/usr/bin/env python3

DISPLAY_BREAKDOWN = ''

def valid_date(s):
    """ Checks if string is the beginning of the day, e.g. 27.02.2017, THURSDAY"""
    if "DAY" in s:
        return s
    else:
        return ""

def valid_time(s):
    """ Checks if string is time record, e.g. 01.55 - 02.10 - Б -
    If yes, returns a tuple with category and length of time in min
    """
    try: 
        start_time = int(s[0:2])*60 + int(s[3:5])
        end_time = int(s[8:10])*60 + int(s[11:13])
        category = s[16:17]
        return (category, end_time - start_time)
    except ValueError:
        return ()

f = open("/Volumes/untitled/План работы.txt", "r",encoding="cp1251")
in_date = False
categories = {}

while True:
    line = f.readline()

    if '===' in line: # if end of all reports
        break

    elif in_date and line == "\n": # if end of report for one day
        for i in "БИРsХ":
            if i in categories:
                print(i, "%2d h %2d min" %(divmod(categories[i],60)))
        print( "Total:", "%d h %d min" %(divmod(sum(categories.values()),60)) )
        in_date = False

    elif valid_date(line): # if it's a start of a day
        print("\n"+line)
        in_date = True
        categories = {}

    elif in_date and valid_time(line): # if we are inside a date
        temp = valid_time(line) 

        if temp[0] == DISPLAY_BREAKDOWN:
            print(line.rstrip())

        if temp[0] in categories:
            categories[temp[0]] += temp[1]
        else:
            categories[temp[0]] = temp[1]
        
f.close()