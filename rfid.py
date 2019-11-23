from time import sleep
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
import time
import os

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("test").sheet1
j = 2
while True:
    sheet.update_cell(j,5,0)
    j = j + 1
    if j == 9:
        break

i = 2
try:
    while True:
        print("Hold a tag near the reader")
        text = reader.read() # Waiting for RFID to tag in
        print("tagged in")
        while True:
            val = float(sheet.cell(i, 1).value)
            if val == text[0]:
                break
            if val == 0:
                sheet.update_cell(i,1,text[0])
                break
            i = i + 1
        check = text[0]
        sheet.update_cell(i,5,1)
        os.system("python3 time.py") # Running the code for the OLED screen
        print("time finished please tag out")
        while True:
            text = reader.read() # Waiiting for RFID to tag out
            if check == text[0]:
                break
            os.system("python tagout.py")
            print("Wrong RFID, use the same tag you used to tag in")
        print("tagged out")
        os.system("python tagin.py") # Running the code to display "Please tag in" on the OLED screen
        sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise
