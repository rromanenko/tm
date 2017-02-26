#!/usr/bin/env python3

def valid_date(s):
    ''' Checks if string is the beginning of the day, i.e. DD.MM.YYYY, [DAY OF WEEK]
    
        Returns: string if it is a start of the day
                 otherwise returns an empty string
    '''
    if "DAY" in s:
        return s
    else:
        return ""

def valid_time(s):
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

    if line == "\n":
        break
    elif valid_date(line):
        print(line)
        in_date = True
        categories = {}
    elif in_date and valid_time(line):
        temp = valid_time(line) 
        if temp[0] in categories:
            categories[temp[0]] += temp[1]
        else:
            categories[temp[0]] = temp[1]

for i in "БИРsХ":
    if i in categories:
        print(i, divmod(categories[i],60))
        
f.close()