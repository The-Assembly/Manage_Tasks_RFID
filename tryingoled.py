from time import sleep
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess

RST = None # Start of required code
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
padding = -2
top = padding
bottom = height-padding
x = 0
font = ImageFont.load_default() # End of required code
draw.rectangle((0,0,width,height), outline=0, fill=0) # Empty screen
draw.text((x, top),       "I",  font=font, fill=255) # Writing text
draw.text((x, top+8),     "Am", font=font, fill=255)
draw.text((x, top+16),    "The",  font=font, fill=255)
draw.text((x, top+24),    "Best",  font=font, fill=255)
disp.image(image) # Display image
disp.display()
sleep(0.1)