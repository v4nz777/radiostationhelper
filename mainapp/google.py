import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('mainapp/creds.json', scope)

client = gspread.authorize(creds)


def add_sheet_for_worker(worker):
    
    spread = client.open("test")
    #ADDING NEW SHEET FOR WORKER
    new_sheet = spread.add_worksheet(title=worker,rows="50", cols="20" )

    #CREATE HEADER FOR NEW SHEET
    #time.sleep(5)
    #open_sheet = client.open("test").worker
    
    
    print(spread.get_all_records())

add_sheet_for_worker("Bong5")

#sheet = client.open("test").sheet1

#insertRow = ["van", "4am", "11pm"]
#sheet.add_rows(2,insertRow)
#sheet.update_cell(5,2, "CHANGED")

print('ok')