from time import sleep
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import RPi.GPIO as GPIO
import subprocess

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
seconds = 0
minutes = 0
hours = 0       
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
    disp.image(image)
    disp.display()
    sleep(0.1)
    if (bb4 == False and i>5): # Breake loop if button 4 is pressed
        break
draw.rectangle((0,0,width,height), outline=0, fill=0)
if c=='x':
    draw.text((x, top),    "job: cleaning",  font=font, fill=255)
if c=='y':
    draw.text((x, top),    "job: coding",  font=font, fill=255)
if c=='z':
    draw.text((x, top),    "job: documenting",  font=font, fill=255)
draw.text((x, top+8),     "time: " + str(hours) + ":" + str(minutes), font=font, fill=255)
draw.text((x, top+16),    "please tag out",  font=font, fill=255)
disp.image(image)
disp.display()
