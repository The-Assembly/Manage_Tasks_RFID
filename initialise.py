import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('Documents/client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("test").sheet1

sheet.update_cell(1,1, 'ID')
sheet.update_cell(1,2, 'Cleaning time in minutes')
sheet.update_cell(1,3, 'Coding time in minutes')
sheet.update_cell(1,4, 'Documenting time in minutes')
sheet.update_cell(1,6, 'Total time in minutes')
sheet.update_cell(1,5, 'Being used')
i = 2
while i <= 9:
    sheet.update_cell(i,1,0)
    sheet.update_cell(i,2,0)
    sheet.update_cell(i,3,0)
    sheet.update_cell(i,4,0)
    sheet.update_cell(i,5,0)
    i = i + 1
    
os.system("python tagin.py") 

