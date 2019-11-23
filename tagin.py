from time import sleep
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess
import os

RST = None     
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST) 
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
draw.text((x, top),       "Please tag in",  font=font, fill=255) # Writing text
disp.image(image) # Display image
disp.display()
sleep(0.1)
os.system("python3 Documents/rfid.py")  # Running the code for the FRID reader




