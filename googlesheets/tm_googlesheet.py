import ezsheets

timeReport = ezsheets.Spreadsheet("1NoLsuFiQkjJoUuCHqFWcfGsQAIxY7tIIKkYxRFU-a0A")
weekReports = timeReport[0]

weekDay = 3
weekDayRow = chr(ord("A") + weekDay)

for i in range(3,9):
    weekReports[weekDayRow + str(i)] = i-3
