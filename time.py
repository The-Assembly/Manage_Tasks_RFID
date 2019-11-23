from time import sleep
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import RPi.GPIO as GPIO
import subprocess

scope = ['https://spreadsheets.google.com/feeds',# google sheets
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("test").sheet1

b4 = 12 # Button declaration
b3 = 16
b2 = 20
b1 = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(b1, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button initialization
GPIO.setup(b2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(b3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(b4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

RST = None     
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST) # OLED screan
disp.begin()
disp.clear()
disp.display()
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0) # Empty screen

padding = -2
top = padding
bottom = height-padding
x = 0
font = ImageFont.load_default()
draw.rectangle((0,0,width,height), outline=0, fill=0) # clear
draw.text((x, top),       "Press one for cleaning",  font=font, fill=255) # Writing text
draw.text((x, top+8),     "Press two for coding", font=font, fill=255)
draw.text((x, top+16),    "Press three for documenting",  font=font, fill=255)
disp.image(image) # Display image
disp.display()
sleep(0.1)
c = '0' # Choosing job

while True:
    bb1 = GPIO.input(b1) # Input from the button
    bb2 = GPIO.input(b2)
    bb3 = GPIO.input(b3)
    bb4 = GPIO.input(b4)
    if bb1 == False: # Button active low
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, top),    "You chose cleaning",  font=font, fill=255)
        draw.text((x, top+8),  "Press four to start", font=font, fill=255)
        sleep(0.1)
        c='x'
    if bb2 == False:
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, top),    "You chose coding",  font=font, fill=255)
        draw.text((x, top+8),  "Press four to start", font=font, fill=255)
        sleep(0.1)
        c='y'
    if bb3 == False:
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, top),    "You chose documenting",  font=font, fill=255)
        draw.text((x, top+8),  "Press four to start", font=font, fill=255)
        sleep(0.1)
        c='z'
    if c != '0':
        if bb4 == False:
            break
    disp.image(image)
    disp.display()
    sleep(0.1)
i=0
j=0
k=0
seconds = 0
minutes = 0
hours = 0
draw.rectangle((0,0,width,height), outline=0, fill=0)
draw.text((x, top),       "Choose Time:",  font=font, fill=255)
draw.text((x, top+8),     "One adds one minute", font=font, fill=255)
draw.text((x, top+16),    "Two adds ten minutes",  font=font, fill=255)
draw.text((x, top+24),    "Three adds one hour",  font=font, fill=255)
disp.image(image)
disp.display()
sleep(1)
m1=0 # Choosing time
h1=0
while True:
    bb1 = GPIO.input(b1) # Input from buttons
    bb2 = GPIO.input(b2)
    bb3 = GPIO.input(b3)
    bb4 = GPIO.input(b4)
    if bb1 == False:
        j=j+1
        sleep(0.1)
    if bb2 == False:
        j=j+10
        sleep(0.1)
    if bb3 == False:
        j=j+60
        sleep(0.1)
    if bb4 == False:
        break
    h1=int(abs(round(j/60-0.49)))
    m1=int(j-h1*60)
    if j!=0:
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, top),       "time:",  font=font, fill=255)
        draw.text((x, top+8),     str(h1) + ":" + str(m1), font=font, fill=255)
        draw.text((x, top+16),    "press four to continue",  font=font, fill=255)
        disp.image(image)
        disp.display()
        
initial = time.time() # Time of start
while True:
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    final = time.time() # Current time
    bb4 = GPIO.input(b4)
    
    draw.text((x, top),       "total time:",  font=font, fill=255)
    draw.text((x, top+8),     str(hours) + ":" + str(minutes) + ":" + str(seconds), font=font, fill=255)
    draw.text((x, top+16),    "the job you chose:",  font=font, fill=255)
    if c=='x':
        draw.text((x, top+24),    "cleaning",  font=font, fill=255) # Selected job
    if c=='y':
        draw.text((x, top+24),    "coding",  font=font, fill=255)
    if c=='z':
        draw.text((x, top+24),    "documenting",  font=font, fill=255)
    
    i=round(final-initial) # Total seconds
    hours = int(abs(round(i/3600-0.499))) # Calculating hours
    minutes = int(abs(round((i-hours*3600)/60-0.499))) # Calculating minutes
    seconds = int(i-hours*3600-60*minutes) # Calculating seconds
    if (m1==minutes and h1==hours):
        break
    disp.image(image)
    disp.display()
    sleep(0.1)
    if (bb4 == False and i>5): # Breake loop if button 4 is pressed
        k=1
        break
draw.rectangle((0,0,width,height), outline=0, fill=0)
if c=='x':
    draw.text((x, top),    "job: cleaning",  font=font, fill=255)
if c=='y':
    draw.text((x, top),    "job: coding",  font=font, fill=255)
if c=='z':
    draw.text((x, top),    "job: documenting",  font=font, fill=255)
if k==0:
    draw.text((x, top+8),    "completion: YES",  font=font, fill=255)
if k==1:
    draw.text((x, top+8),    "completion: NO",  font=font, fill=255)
draw.text((x, top+16),     "time: " + str(hours) + ":" + str(minutes), font=font, fill=255)
draw.text((x, top+24),    "please tag out",  font=font, fill=255)
disp.image(image)
disp.display()
i = 2
while True:
        val = float(sheet.cell(i, 5).value)
        if val == 1:
            if c == 'x':
                sheet.update_cell(i,2,minutes + hours*60 + float(sheet.cell(i, 2).value))
            if c == 'y':
                sheet.update_cell(i,3,minutes + hours*60 + float(sheet.cell(i, 3).value))
            if c == 'z':
                sheet.update_cell(i,4,minutes + hours*60 + float(sheet.cell(i, 4).value))
            break
        i = i + 1

