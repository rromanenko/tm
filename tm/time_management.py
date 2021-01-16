#!/usr/bin/env python3

import os
import pprint
# import pyperclip
import re
import sys
import time
import zipfile

# false - off, anything else - on
heavy_functions_toggle = True

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

CATEGORIES_RU = "БИРсХ"
CATEGORIES_EN = "BIDsN"

GOOGLESHEET_TIME_REPORT = "1cn8rD8iO22nbr6C5HhEhWyT1ik4_47TUGUaKHi8Rc7M"
GOOGLESHEET_FINANCE_REPORT = "18LBj8iAIwGGdVfn10pq8cDoA-sEF_KKZgAsuEQ6Kwd8"

WEEK_REPORTS_SHEET = "Week reports"
# Google API's can be disabled at https://console.developers.google.com/apis/dashboard?project=quickstart-1592851518682

workplan = "План работы.txt"
backup_file = "personalBackup.zip"
personal_files = ["life.txt", "План работы.txt", "Цели.txt"]
metrics_list = [("tmyself",), ("back and eye", "abs", "palming")]
calculated_metrics = {"yoga": 0}


def log_chess_time(log_time):
    import requests
    from requests.auth import HTTPBasicAuth
    import json

    url = "https://rroman.atlassian.net/rest/api/latest/issue/MY-853/worklog"
    auth = HTTPBasicAuth(username, token)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = json.dumps({"timeSpentSeconds": log_time * 60})

    response = requests.request(
        "POST",
        url,
        data=payload,
        headers=headers,
        auth=auth
    )

    if response.status_code == 201:
        print(f" {log_time} min logged in successfully!")
    else:
        print(f"Error: {response.status_code}")
        print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))


def backup_tm_and_fm_reports(path):
    """ This function downloads Time & Finance Management reports from Google Drive to a local folder /Personal
    """
    tm = ezsheets.Spreadsheet(GOOGLESHEET_TIME_REPORT)
    fm = ezsheets.Spreadsheet(GOOGLESHEET_FINANCE_REPORT)

    os.chdir(path + "/Personal")
    print(f"Saving {tm.title} and {fm.title} at {path + 'Personal'} ...")
    tm.downloadAsExcel()
    fm.downloadAsExcel()
    print("Done.")
    os.chdir(path)


def save_metrics_to_googlesheet(daily_metrics, week_day):
    """ This function saves results for metrics_list into Time Management file.
    Input:  daily metrics is a dictionary { metric: number of times it occurred during the day }
            week_day is day of the week where Monday = 1, etc
    """
    week_reports = ezsheets.Spreadsheet(GOOGLESHEET_TIME_REPORT)[WEEK_REPORTS_SHEET]
    print(f"Saving metrics to {week_reports.title} ...")

    # skipping rows with categories, starting with rows where metrics start
    starting_row = 2 + len(CATEGORIES_EN) + 3

    weekday_column = chr(ord("A") + week_day)

    # go through metrics until we reach an empty row
    # if any of the metric equals to another metric in the metric dictionary, save it to the cell for the respective day
    while week_reports['A' + str(starting_row)]:
        for value in daily_metrics:
            if str(",".join(value)) == week_reports['A' + str(starting_row)]:
                week_reports[weekday_column + str(starting_row)] = daily_metrics[value]
        starting_row += 1
    print("Done.")


def save_results_to_googlesheet(daily_results, week_day):
    """ This function saves results for the day into Time Management file.
    Input: "5.5\n6.83\n..." and weekday number where Monday = 1
    Top-left corner is B3, that's why we have to shift from A1 to chr(ord("A") + week_day) and num + 3
    """
    week_reports = ezsheets.Spreadsheet(GOOGLESHEET_TIME_REPORT)[WEEK_REPORTS_SHEET]
    print(f"Saving daily results to {week_reports.title} ...")

    weekday_column = chr(ord("A") + week_day)
    for num, category_time in enumerate(daily_results.split("\n")[:-1]):
        week_reports[weekday_column + str(num + 3)] = category_time
    print("Done.")


def valid_time(s):
    """ Checks if the string is a time record with a category, e.g. 01.55 - 02.10 - Б -
    If yes, returns a tuple with category and length of time in min
    """
    valid_time_line = re.compile(r'^(\d\d).(\d\d) - (\d\d).(\d\d) - (.)').search(s)

    if valid_time_line:
        start_hour, start_min, end_hour, end_min, time_category = valid_time_line.groups()

        if time_category not in CATEGORIES_EN + CATEGORIES_RU:
            raise Exception("Unknown category [" + time_category + "] in line: " + s)

        # if category is entered in English, convert it to Russian
        if time_category in CATEGORIES_EN:
            time_category = CATEGORIES_RU[CATEGORIES_EN.find(time_category)]

        return time_category, int(end_hour) * 60 + int(end_min) - int(start_hour) * 60 - int(start_min)
    else:
        return ()


def valid_secondary_category(s):
    """ Checks if line contains a secondary category, e.g. 01.55 - 02.10 - Б - ix:
    Here "ix" is a secondary category, separated with ":" sign
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


def create_backup(backup_path, backup_file, file_list):
    backup = zipfile.ZipFile(backup_path + backup_file, "w")
    for f in file_list:
        # backup.write(backup_path + f, compress_type=zipfile.ZIP_DEFLATED)
        backup.write(backup_path + f)
    backup.close()


if __name__ == "__main__":

    # get current working directory depending on if we are on mac or windows
    cwd = get_path()

    try:
        workplan = open(cwd + workplan, "r", encoding="cp1251")
    except FileNotFoundError:
        print(f"File {workplan} not found at {cwd}!")
        exit()

    in_date = False
    weekDay = 0

    while True:
        line = workplan.readline()

        # if we are inside a day, check lines for metrics you want to track
        if in_date and line != '\n':
            for metrics_tuple in metrics_list:
                for metric in metrics_tuple:
                    if metric in line.lower():
                        metrics[metrics_tuple] += line.lower().count(metric)

            for metric in calculated_metrics:
                s = line.lower()
                while metric in s:
                    start = s.find('(', s.find(metric))
                    end = s.find(')', s.find(metric))
                    if start != -1 and end != -1:
                        try:
                            calculated_metrics[metric] += int(s[start + 1: end])
                        except ValueError:
                            pass
                    else:
                        break
                    s = s[end+1:]

        # if end of all daily reports
        if line.startswith('====='):
            break

        # if the line starts with something like "27.02.2017, MONDAY", it's a start of a new day
        elif re.compile(rf'^\d\d.\d\d.\d\d\d\d, MONDAY|TUESDAY|WEDNESDAY|THURSDAY|FRIDAY|SATURDAY|SUNDAY').search(line):
            print("\n" + Blue + line + White, end="")
            in_date = True
            prev_time = ""
            categories = {}
            secondary_categories = {}
            total_cal = []
            metrics = {i: 0 for i in metrics_list}
            calculated_metrics = {i: 0 for i in calculated_metrics}

            # Determining the number of the day of the week, where Monday is 1, Tuesday is 2, and so on
            weekDay = 1 + ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"].index(line.split()[1])

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

        # if end of report for the day, print time for each category
        elif in_date and line == "\n":

            dailyResults = ""
            for counter, value in enumerate(CATEGORIES_RU):
                calculatedTime = str(round(categories.get(value, 0) // 60 + categories.get(value, 0) % 60 / 60, 4))
                # saving daily metrics without categories, so we could copy them to clipboard later
                dailyResults += calculatedTime + "\n"
                # .. and printing the to screen as well
                print(value + ": " + calculatedTime)

            # Adding calculated_metrics dictionary to metrics dict
            # As metrics dict elements are tuple:value, while calculated metrics are string:value,
            # we can't simply combine dicts and have to add them through a cycle
            for i in calculated_metrics.keys():
                metrics[(i,)] = calculated_metrics[i]

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
                # mo = re.compile(r'\d+.\d+').findall(pyperclip.paste())
                # if not mo or len(mo) != len(CATEGORIES_RU):
                #     pyperclip.copy(dailyResults)

                # if backup zip is empty or doesn't exist or any file in this zip differs from files on disk,
                # then zip the personal files
                flag = False
                try:
                    backupZip = zipfile.ZipFile(cwd + backup_file)
                    if not backupZip.namelist():
                        flag = True

                    for file in backupZip.namelist():
                        if os.path.getsize("/" + file) != backupZip.getinfo(file).file_size:
                            flag = True
                            break
                except FileNotFoundError:
                    flag = True

                if flag:
                    create_backup(cwd, backup_file, personal_files)
                    print(f"{personal_files} zipped in {backup_file} at {cwd}, size {os.path.getsize(cwd+backup_file)}")

                if heavy_functions_toggle:
                    try:
                        import ezsheets
                        save_results_to_googlesheet(dailyResults, weekDay)
                        save_metrics_to_googlesheet(metrics, weekDay)
                        time.sleep(60)
                        backup_tm_and_fm_reports(cwd)
                    except Exception as e:
                        print("Exception: ", e)

            # print(Purple + "Metrics:", metrics, White)
            if secondary_categories:
                print(Orange, end="")
                pprint.pprint(secondary_categories)
                print(White)
                if ("Р", "chess") in secondary_categories:
                    a = input(f"Do you want to log {secondary_categories[('Р', 'chess')]} min to chess epic (y/n)?: ")
                    if a.lower().startswith("y"):
                        log_chess_time(secondary_categories[("Р", "chess")])

            # print(Purple+"Calories for the day:", total_cal, sum(total_cal))

            in_date = False

    workplan.close()
