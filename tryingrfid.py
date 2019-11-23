from time import sleep
import sys
from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()
import time
print("Hold a tag near the reader")
try:
    while True:
        
        text = reader.read() # Waiting for RFID to tag in
        print "RFID number: ", text[0] # Display the RFID number
        sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise








