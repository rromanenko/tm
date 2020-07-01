#!/usr/bin/env python3

import os
import pprint
import pyperclip
import re
import sys
import zipfile

# choose what category to display
DISPLAY_BREAKDOWN = 'ХN'
# DISPLAY_BREAKDOWN = 'BБ'
# DISPLAY_BREAKDOWN = 'ИI'
# DISPLAY_BREAKDOWN = 'Р'

White = '\033[0m'
Red = '\033[31m'
Green = '\033[32m'
Orange = '\033[33m'
Blue = '\033[34m'
Purple = '\033[35m'

cat_ru = "БКИРсХ"
cat_en = "BCIDsN"

workplan = "План работы.txt"
backup_file = "personalBackup.zip"
personal_files = ["life.txt", "План работы.txt", "Цели.txt"]

metrics_list = [("tmyself",), ("push-up", "pull-up", "yoga")]


def valid_time(s):
    """ Checks if string is a time record with a category, e.g. 01.55 - 02.10 - Б -
    If yes, returns a tuple with category and length of time in min
    """
    valid_time_line = re.compile(r'^(\d\d).(\d\d) - (\d\d).(\d\d) - (.)').search(s)

    if valid_time_line:
        start_hour, start_min, end_hour, end_min, time_category = valid_time_line.groups()

        if time_category not in cat_en + cat_ru:
            raise Exception("Unknown category [" + time_category + "] in line: " + s)

        # if category is entered in English, convert it to Russian
        if time_category in cat_en:
            time_category = cat_ru[cat_en.find(time_category)]

        return time_category, int(end_hour) * 60 + int(end_min) - int(start_hour) * 60 - int(start_min)
    else:
        return ()


def valid_secondary_category(s):
    """ Checks if line contains a secondary category, i.e. ix, e.g. 01.55 - 02.10 - Б - ix:
    If yes, returns a tuple ((primary category, secondary category), duration), else returns an empty string
    """
    if ":" in s:
        return (valid_time(s)[0], s[20:s.find(":")]), valid_time(s)[1]
    else:
        return ()


def get_path():
    if sys.platform == "darwin":
        return "/Volumes/untitled/"
    elif sys.platform == "win32":
        return "C:/Мои документы/"
    else:
        print("Unknown platform:", sys.platform)
        exit()


def create_backup(backup_path, file_list):
    backup = zipfile.ZipFile(backup_path, "w")
    for f in file_list:
        # backupZip.write(file, compress_type=zipfile.ZIP_DEFLATED)
        backup.write(f)
    backup.close()


if __name__ == "__main__":

    # set current working directory depending on if we are on mac or windows
    # then open this directory
    cwd = get_path()
    os.chdir(cwd)

    try:
        workplan = open(cwd + workplan, "r", encoding="cp1251")
    except FileNotFoundError:
        print(f"File {workplan} at {cwd} not found!")
        exit()

    in_date = False

    while True:
        line = workplan.readline()

        # if we are inside a day, check lines for metrics you want to track
        if in_date and line != '\n':
            for metrics_tuple in metrics_list:
                for metric in metrics_tuple:
                    if metric in line.lower():
                        metrics[metrics_tuple] += line.lower().count(metric)

        # if end of all daily reports
        if line.startswith('====='):
            break

        # if the line starts with something like "27.02.2017,", it's a start of a new day
        elif re.compile(rf'^\d\d.\d\d.\d\d\d\d,').search(line):
            print("\n" + Blue + line + White, end="")
            in_date = True
            prev_time = ""
            categories = {}
            secondary_categories = {}
            total_cal = []
            metrics = {i: 0 for i in metrics_list}

        # if there's a number of eaten calories in the line
        elif "kcal" in line:
            line = line.rstrip().replace(".", " ").split()
            total_cal += [int(line[line.index('kcal') - 1])]

        # if we are inside a day and line is a line with time
        elif in_date and valid_time(line):
            category, duration = valid_time(line)

            # check for not 24 h error. If times of adjacent activities don't match, i.e. it's not
            # xx.xx - xx.15
            # xx.15 - xx.xx
            # print the line
            if prev_time != "" and line[3:5] != prev_time:
                print(Red + line, White)
            prev_time = line[11:13]

            if category in DISPLAY_BREAKDOWN:
                print(line.rstrip())

            # check if category is already added to categories dict, if not, create it and add duration as 0
            # then increase its duration
            categories.setdefault(category, 0)
            categories[category] += duration

            if valid_secondary_category(line):
                second_cat, second_cat_duration = valid_secondary_category(line)
                secondary_categories.setdefault(second_cat, 0)
                secondary_categories[second_cat] += second_cat_duration

        # if end of report for one day, print time for each category
        elif in_date and line == "\n":
            # saving daily metrics without categories, so we could copy them to clipboard later
            daily_results = "\n".join([str(round(categories.get(i, 0) // 60 + categories.get(i, 0) % 60 / 60, 4))
                                       for i in cat_ru])

            for i in cat_ru:
                print(i + ": " + str(round(categories.get(i, 0) // 60 + categories.get(i, 0) % 60 / 60, 4)))

            # if total is not "24 h 0 min", then print Total in different color
            (hours, minutes) = divmod(sum(categories.values()), 60)
            if (hours, minutes) != (24, 0):
                print(Red + "Total:", f"{hours} h {minutes} min", White)
            else:
                print(Green + "Total:", f"{hours} h", White)

                # here we check if clipboard already contains data similar to daily results
                # for this we search for patterns like 00.15 in clipboard
                # if there are no such patterns in clipboard, or # of them doesn't equal to # of categories
                # then we save daily result to clipboard
                mo = re.compile(r'\d+.\d+').findall(pyperclip.paste())
                if not mo or len(mo) != len(cat_ru):
                   pyperclip.copy(daily_results)

                # if backup zip doesn't exist or any file in this zip differs from files on disk, zip the files
                try:
                    backupZip = zipfile.ZipFile(cwd + backup_file)
                    for file in backupZip.namelist():
                        if os.path.getsize(file) != backupZip.getinfo(file).file_size:
                            create_backup(cwd + backup_file, personal_files)
                            break
                except FileNotFoundError:
                    create_backup(cwd + backup_file, personal_files)

            print(Purple + "Metrics:", metrics, White)

            if secondary_categories:
                print(Orange, end="")
                pprint.pprint(secondary_categories)
                print(White)

            # print(Purple+"Calories for the day:", total_cal, sum(total_cal))
            in_date = False

    workplan.close()
