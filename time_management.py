 #!/usr/bin/env python3

DISPLAY_BREAKDOWN = 'Х' # if you want to display some category

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple

#def valid_date(s):
#    """ Checks if string is the beginning of the day, e.g. 27.02.2017, THURSDAY"""
#    return "DAY" in s

def valid_time(s):
    """ Checks if string is a time record, e.g. 01.55 - 02.10 - Б -
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
#categories = {}

while True:
    line = f.readline()

    if '===' in line: # if end of all daily reports
        break

    elif "DAY" in line: # if it's a start of a day, e.g. 27.02.2017, THURSDAY"""
        print("\n"+B+line+W)
        in_date = True
        prev_time = ""
        categories = {}

    elif in_date and valid_time(line): # if we are inside a date and line is a line with time
        temp = valid_time(line) 

        # check for not 24h00 error. If not
        # xx.xx- xx.15
        # xx.15 - xx.xx
        # print the line
        if prev_time != "" and line[3:5] != prev_time:
            color = R
            print(color+line, W)
        prev_time = line[11:13]

        if temp[0] == DISPLAY_BREAKDOWN:
            print(line.rstrip())

        if temp[0] in categories:
            categories[temp[0]] += temp[1]
        else:
            categories[temp[0]] = temp[1]

    elif in_date and line == "\n": # if end of report for one day
        for i in "БИРsХ":
            if i in categories:
#                print(i, "%2d h %2d min / " %(divmod(categories[i],60)), end="")
                print( round(categories[i] // 60 + categories[i] % 60 / 60, 4))

        # if total is not "24 h 0 min", then print Total in different color
        (hours, minutes) = divmod(sum(categories.values()),60)
        if (hours, minutes) == (24, 0):
            color = G
        else:
            color = R
        print( color+"Total:", "%d h %d min" %(hours, minutes), W )
        in_date = False
        
f.close()
