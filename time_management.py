#!/usr/bin/env python3

import pyperclip
import re
import sys

# choose what category to display
DISPLAY_BREAKDOWN = 'ХN'
# DISPLAY_BREAKDOWN = 'BБ'
# DISPLAY_BREAKDOWN = 'ИI'


White = '\033[0m'
Red = '\033[31m'
Green = '\033[32m'
Orange = '\033[33m'
Blue = '\033[34m'
Purple = '\033[35m'

cat_ru = "БКИРсХ"
cat_en = "BCIDsN"

metrics_list = ["touched myself", "push-up", "pull-up", "yoga"]


def valid_time(s):
    """ Checks if string is a time record with a category, e.g. 01.55 - 02.10 - Б -
    If yes, returns a tuple with category and length of time in min
    """
    mo = re.compile(rf'^(\d\d).(\d\d) - (\d\d).(\d\d) - ([{cat_en+cat_ru}])').search(s)
    if mo:
        start_hour, start_min, end_hour, end_min, category = mo.groups()
        return category, int(end_hour) * 60 + int(end_min) - int(start_hour) * 60 - int(start_min)
    else:
        return ()


# Windows sys.platform is "win32"
path = "C:/Мои документы/План работы.txt"
if sys.platform == "darwin":
    path = "/Volumes/untitled/План работы.txt"

try:
    f = open(path, "r", encoding="cp1251")
except FileNotFoundError:
    print(f"File План работы at {path} not found!")
    exit()

in_date = False

while True:
    line = f.readline()

    for metric in metrics_list:
        if metric in line.lower():
            metrics[metric] += line.lower().count(metric)

    # if end of all daily reports
    if line.startswith('====='):
        break

    # if it's a start of a day, e.g. 27.02.2017, THURSDAY"""
    elif "DAY" in line:
        print("\n"+Blue+line+White)
        in_date = True
        prev_time = ""
        categories = {}
        total_cal = []
        metrics = {i: 0 for i in metrics_list}

    # if there's a number of eaten calories in the line
    elif "kcal" in line:
        line = line.rstrip().replace(".", " ").split()
        total_cal += [int(line[line.index('kcal')-1])]

    # if we are inside a date and line is a line with time
    elif in_date and valid_time(line):
        category, duration = valid_time(line)

        # check for not 24h00 error. If not
        # xx.xx - xx.15
        # xx.15 - xx.xx
        # print the line
        if prev_time != "" and line[3:5] != prev_time:
            color = Red
            print(color+line, White)
        prev_time = line[11:13]

        if category in cat_en:
            category = cat_ru[cat_en.find(category)]
    
        if category in DISPLAY_BREAKDOWN:
            print(line.rstrip())

        # check if category is already added to categories dict, if not, create it and add duration as 0
        # then increase its duration
        categories.setdefault(category, 0)
        categories[category] += duration

    # if end of report for one day, print time for each category
    elif in_date and line == "\n":
        daily_results = "\n".join([str(round(categories.get(i, 0) // 60 + categories.get(i, 0) % 60 / 60, 4))
                                   for i in cat_ru])
        print(daily_results)

        # saving daily results for each category into computer clipboard
        # first checking if clipboard already contains data similar to daily results. if so, don't save anything.
        # len(cat_ru) - 1 because last item doesn't have \n ['0.3333\n', '3.0\n', '7.0\n', '6.5\n', '6.4167\n']
        mo = re.compile(r'\d+.\d+\n').findall(pyperclip.paste())
        if not mo or len(mo) != len(cat_ru) - 1:
            pyperclip.copy(daily_results)

        # if total is not "24 h 0 min", then print Total in different color
        (hours, minutes) = divmod(sum(categories.values()), 60)
        if (hours, minutes) == (24, 0):
            print(Green + "Total:", f"{hours} h", White)
        else:
            print(Red + "Total:", f"{hours} h {minutes} min", White)

        print(Purple + "Metrics: ", metrics)
        # print(Purple+"Calories for the day:", total_cal, sum(total_cal))
        in_date = False
        
f.close()
