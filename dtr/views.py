
from datetime import datetime
from os import path

from .helper import create_new_workbook, log_user_to_workbook




def worklogger(worker):
    
    today = datetime.now()
    month = today.strftime("%B")

    in_or_out = "IN"

    #IF NO WORKBOOK CREATED
    if not path.exists(f"dtr/output/{month}_{today.year}.xlsx"):
        create_new_workbook()
        
        if today.strftime("%p") == 'AM':
            clock_in_pos = f'C{16 + today.day}'
            midnight = False
            log_user_to_workbook(in_or_out, worker,clock_in_pos, midnight)

        elif today.strftime("%p") == 'PM':
            clock_in_pos = f'E{16 + today.day}'
            midnight = False
            log_user_to_workbook(in_or_out, worker,clock_in_pos, midnight)

        elif today.strftime("%p") == 'AM' and today.strftime("%I") == '12':
            clock_in_pos = f'E{16 + today.day}'
            midnight = True
            log_user_to_workbook(in_or_out, worker,clock_in_pos, midnight)

    #IF WORKBOOK EXIST
    else:
        if today.strftime("%p") == 'AM':
            clock_in_pos = f'C{16 + today.day}'
            midnight = False
            log_user_to_workbook(in_or_out, worker,clock_in_pos, midnight)
            

        elif today.strftime("%p") == 'PM':
            clock_in_pos = f'E{16 + today.day}'
            midnight = False
            log_user_to_workbook(in_or_out, worker,clock_in_pos, midnight)
        
        elif today.strftime("%p") == 'AM' and today.strftime("%I") == '12':
            clock_in_pos = f'E{16 + today.day}'
            midnight = True
            log_user_to_workbook(in_or_out, worker,clock_in_pos, midnight)

    

def worklogger_out(worker):
    today = datetime.now()
    month = today.strftime("%B")

    clock_in_pos = f'B{today.day}'
    in_or_out = "OUT"
    #IF NO WORKBOOK CREATED
    if not path.exists(f"dtr/output/{month}_{today.year}.xlsx"):
        create_new_workbook()
        
        if today.strftime("%p") == 'AM':
            clock_in_pos = f'D{16 + today.day}'
            midnight = False
            log_user_to_workbook(in_or_out, worker,clock_in_pos, midnight)

        elif today.strftime("%p") == 'PM':
            clock_in_pos = f'F{16 + today.day}'
            midnight = False
            log_user_to_workbook(in_or_out, worker,clock_in_pos, midnight)
        
        elif today.strftime("%p") == 'AM' and today.strftime("%I") == '12':
            clock_in_pos = f'F{16 + today.day}'
            midnight = True
            log_user_to_workbook(in_or_out, worker,clock_in_pos, midnight)

    #IF WORKBOOK EXIST
    else:
        if today.strftime("%p") == 'AM':
            clock_in_pos = f'D{16 + today.day}'
            midnight = False
            log_user_to_workbook(in_or_out, worker,clock_in_pos, midnight)

        elif today.strftime("%p") == 'PM':
            clock_in_pos = f'F{16 + today.day}'
            midnight = False
            log_user_to_workbook(in_or_out, worker,clock_in_pos, midnight)
        
        elif today.strftime("%p") == 'AM' and today.strftime("%I") == '12':
            clock_in_pos = f'F{16 + today.day}'
            midnight = True
            log_user_to_workbook(in_or_out, worker,clock_in_pos, midnight)



#bio = openpyxl.load_workbook("dtr/bio.xlsx")

#active_sheet = bio.active


#c1 = active_sheet.cell(row = 1, column = 1) 

#c1.value = "Name"

#bio.save("dtr/file.xlsx")

