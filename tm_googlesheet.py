import ezsheets

timeReport = ezsheets.Spreadsheet("1cn8rD8iO22nbr6C5HhEhWyT1ik4_47TUGUaKHi8Rc7M")

# print(timeReport.title)
# print(timeReport.spreadsheetId)
# print(timeReport.url)
# print(timeReport.sheetTitles)
# print(timeReport.sheets)
print(timeReport["Week reports"])

#timeReport.downloadAsExcel()

# print( ezsheets.listSpreadsheets() )