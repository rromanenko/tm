#!/usr/bin/env python3

#DISPLAY_BREAKDOWN = 'ХN' # if you want to display some category
DISPLAY_BREAKDOWN = 'BБ' # if you want to display some category
#DISPLAY_BREAKDOWN = 'ИI' # if you want to display some category
#DISPLAY_BREAKDOWN = 'Р' # if you want to display some category

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple

cat_ru = "БИРsХ"
cat_en = "BIDsN"

metrics_list = ["lean software", "myself", "back exercises", "palming"]

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

f = open("/Volumes/untitled/План работы.txt", "r", encoding="cp1251")
in_date = False

while True:
    line = f.readline()

    for metric in metrics_list:
        if metric in line.lower():
            metrics[metric] += line.lower().count(metric)

    if '=====' in line: # if end of all daily reports
        break

    elif "DAY" in line: # if it's a start of a day, e.g. 27.02.2017, THURSDAY"""
        print("\n"+B+line+W)
        in_date = True
        prev_time = ""
        categories = {}
        total_cal = []
        metrics = { i: 0 for i in metrics_list }

    elif "kcal" in line: # if there's a number of eaten calories in the line
        line = line.rstrip().replace(".", " ").split()
        total_cal += [int(line[line.index('kcal')-1] )]

    elif in_date and valid_time(line): # if we are inside a date and line is a line with time
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

    elif in_date and line == "\n": # if end of report for one day
        for i in "БИРsХ":
            if i in categories:
#                print(i, "%2d h %2d min / " %(divmod(categories[i],60)), end="")
                print( round(categories[i] // 60 + categories[i] % 60 / 60, 4))
            else:
                print(0)

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
