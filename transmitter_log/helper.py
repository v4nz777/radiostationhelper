from openpyxl import load_workbook
from datetime import datetime
import shutil
import os


TRANSMITTER_LOG_TEMPLATE = os.path.abspath('transmitter_log/output/template_transmitter_log.xlsx')

def transmitter_open_and_log(current_workbook,
                                sheet_name,
                                voltage,
                                exciter,
                                driver_ipa,
                                driver_fwd_pwr,
                                driver_rfl_pwr,
                                vpa,
                                final_ipa,
                                final_fwd_pwr,
                                final_rfl,
                                remarks,
                                sign_on_time,
                                populate_previous
                                ):
    workbook = load_workbook(current_workbook)
    sheet = workbook[sheet_name]
    
    write_data_int(sheet, 'B', voltage, sign_on_time, populate_previous=populate_previous)
    write_data_int(sheet, 'C', exciter, sign_on_time, populate_previous=populate_previous)
    write_data_int(sheet, 'D', driver_ipa, sign_on_time, populate_previous=populate_previous)
    write_data_int(sheet, 'E', driver_fwd_pwr, sign_on_time, populate_previous=populate_previous)
    write_data_int(sheet, 'F', driver_rfl_pwr, sign_on_time, populate_previous=populate_previous)
    write_data_int(sheet, 'G', vpa, sign_on_time, populate_previous=populate_previous)
    write_data_int(sheet, 'H', final_ipa, sign_on_time, populate_previous=populate_previous)
    write_data_int(sheet, 'I', final_fwd_pwr, sign_on_time, populate_previous=populate_previous)
    write_data_int(sheet, 'J', final_rfl, sign_on_time, populate_previous=populate_previous)
    write_data_int(sheet, 'K', remarks, sign_on_time, populate_previous=populate_previous)

    workbook.save(current_workbook)
    print('SUCCESSFULLY TRANSMITTER LOGGED')





def write_data_int(sheet, cell, data, sign_on_time, populate_previous):
    #fill fields before sign on
    #except 24 hours operation
    if sign_on_time != 1:
        sheet[f'{cell}{11+int(sign_on_time)-1}'].value = 'off'

    time = datetime.now().strftime("%H")
    
    if data == "":
        num = 1
        while sheet[f'{cell}{11+int(time)-num}'].value == None:
            num += 1
            sheet[f'{cell}{11+int(time)}'].value = sheet[f'{cell}{11+int(time)-num}'].value  
            
    else:
        if cell == 'B':
            sheet[f'{cell}{11+int(time)}'].value = data+'v'
        elif cell == 'C':
            sheet[f'{cell}{11+int(time)}'].value = data+'w'
        elif cell == 'D':
            sheet[f'{cell}{11+int(time)}'].value = data+'a'
        elif cell == 'E':
            sheet[f'{cell}{11+int(time)}'].value = data+'w'
        elif cell == 'F':
            sheet[f'{cell}{11+int(time)}'].value = data+'w'
        elif cell == 'G':
            sheet[f'{cell}{11+int(time)}'].value = data+'v'
        elif cell == 'H':
            sheet[f'{cell}{11+int(time)}'].value = data+'a'
        elif cell == 'I':
            sheet[f'{cell}{11+int(time)}'].value = data+'w'
        elif cell == 'J':
            sheet[f'{cell}{11+int(time)}'].value = data+'w'
    
    if populate_previous:
        print('Populating Previous Hours')
        n = 1
        while sheet[f'{cell}{11+int(time)-n}'].value == None and cell != 'K':
            #sheet[f'{cell}{11+int(time)-n}'].value = data
            if cell == 'B':
                sheet[f'{cell}{11+int(time)-n}'].value = data+'v'
            elif cell == 'C':
                sheet[f'{cell}{11+int(time)-n}'].value = data+'w'
            elif cell == 'D':
                sheet[f'{cell}{11+int(time)-n}'].value = data+'a'
            elif cell == 'E':
                sheet[f'{cell}{11+int(time)-n}'].value = data+'w'
            elif cell == 'F':
                sheet[f'{cell}{11+int(time)-n}'].value = data+'w'
            elif cell == 'G':
                sheet[f'{cell}{11+int(time)-n}'].value = data+'v'
            elif cell == 'H':
                sheet[f'{cell}{11+int(time)-n}'].value = data+'a'
            elif cell == 'I':
                sheet[f'{cell}{11+int(time)-n}'].value = data+'w'
            elif cell == 'J':
                sheet[f'{cell}{11+int(time)-n}'].value = data+'w'
            n+=1




def transmitter_logging(voltage,
                        exciter,
                        driver_ipa,
                        driver_fwd_pwr,
                        driver_rfl_pwr,
                        vpa,
                        final_ipa,
                        final_fwd_pwr,
                        final_rfl,
                        remarks,
                        sign_on_time,
                        populate_previous
                        ):

    today = datetime.now()
    month = today.strftime("%B")
    year = today.strftime("%Y")

    #IF NO WORKBOOK FOUND, COPY TEMPLATE WORKBOOK AND OPEN IT
    current_workbook = os.path.abspath(f'transmitter_log/output/{month}_{year}.xlsx')
    if not os.path.exists(current_workbook):
        print('COPYING TEMPLATE AND RENAMING...')
        shutil.copyfile(TRANSMITTER_LOG_TEMPLATE, current_workbook)
        print(f'{current_workbook} workbook created!!!')

        sheet_name = today.strftime("%d")
        transmitter_open_and_log(current_workbook,
                                    sheet_name,
                                    voltage,
                                    exciter,
                                    driver_ipa,
                                    driver_fwd_pwr,
                                    driver_rfl_pwr,
                                    vpa,
                                    final_ipa,
                                    final_fwd_pwr,
                                    final_rfl,
                                    remarks,
                                    sign_on_time,
                                    populate_previous
                                    )
        
    else:
        sheet_name = today.strftime("%d")
        transmitter_open_and_log(current_workbook,
                                    sheet_name,
                                    voltage,
                                    exciter,
                                    driver_ipa,
                                    driver_fwd_pwr,
                                    driver_rfl_pwr,
                                    vpa,
                                    final_ipa,
                                    final_fwd_pwr,
                                    final_rfl,
                                    remarks,
                                    sign_on_time,
                                    populate_previous
                                    )