#!/usr/bin/env python3

DISPLAY_BREAKDOWN = 'ХN' # if you want to display some category
#DISPLAY_BREAKDOWN = 'BБ' # if you want to display some category
#DISPLAY_BREAKDOWN = 'ИI' # if you want to display some category
#DISPLAY_BREAKDOWN = 'H' # if you want to display some category

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purpler

cat_ru = "БИРсХ"
cat_en = "BIDsN"

metrics_list = ["touched myself", "push-up", "pull-up", "yoga"]

def valid_time(s):
    """ Checks if string is a time record, e.g. 01.55 - 02.10 - Б -
    If yes, returns a tuple with category and length of time in min
    """
    try:
        start_time = int(s[0:2])*60 + int(s[3:5])
        end_time = int(s[8:10])*60 + int(s[11:13])
        category = s[16:17]
        if category in (cat_en + cat_ru):
            return (category, end_time - start_time)
        return ()
    except ValueError:
        return ()

#try to open the time management file
#check if we are on Mac or Windows
try:
    path = "/Volumes/untitled/План работы.txt"
    f = open(path, "r", encoding="cp1251")
except FileNotFoundError:
    try:
        path = "C:\Мои документы\План работы.txt"
        f = open(path, "r", encoding="cp1251")
    except FileNotFoundError:
        print("File План работы not found!")
        exit()

in_date = False

while True:
    line = f.readline()

    for metric in metrics_list:
        if metric in line.lower():
            metrics[metric] += line.lower().count(metric)

    # if end of all daily reports
    if '=====' in line:
        break

    # if it's a start of a day, e.g. 27.02.2017, THURSDAY"""
    elif "DAY" in line:
        print("\n"+B+line+W)
        in_date = True
        prev_time = ""
        categories = {}
        total_cal = []
        metrics = { i: 0 for i in metrics_list }

    # if there's a number of eaten calories in the line
    elif "kcal" in line:
        line = line.rstrip().replace(".", " ").split()
        total_cal += [int(line[line.index('kcal')-1] )]

    # if we are inside a date and line is a line with time
    elif in_date and valid_time(line):
        category, duration = valid_time(line)

        # check for not 24h00 error. If not
        # xx.xx - xx.15
        # xx.15 - xx.xx
        # print the line
        if prev_time != "" and line[3:5] != prev_time:
            color = R
            print(color+line, W)
        prev_time = line[11:13]

        if category in cat_en:
            category = cat_ru[cat_en.find(category)]
    
        if category in DISPLAY_BREAKDOWN:
            print(line.rstrip())

        if category in categories:
            categories[category] += duration
        else:
            categories[category] = duration

    # if end of report for one day, print time for each category
    elif in_date and line == "\n":
        for i in cat_ru:
            print( round(categories.get(i,0) // 60 + categories.get(i,0) % 60 / 60, 4))
#            print(i, "%2d h %2d min " %(divmod(categories.get(i,0),60)))

        # if total is not "24 h 0 min", then print Total in different color
        (hours, minutes) = divmod(sum(categories.values()),60)
        if (hours, minutes) == (24, 0):
            color = G
        else:
            color = R
        print( color+"Total:", "%d h %d min" %(hours, minutes), W )
        color = P
        print(color+"Metrics: ", metrics)
        #print(color+"Calories for the day:", total_cal, sum(total_cal))
        in_date = False
        
f.close()