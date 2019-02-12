import i2cOLED
import framebuf
from time import sleep

def display_image(fileToDisplay):

    with open(fileToDisplay, 'rb') as f:
        f.readline() # Magic number
        f.readline() # Creator comment
        f.readline() # Dimensions
        data = bytearray(f.read())
    fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
    # make sure, your image is inverted
    # if not, invert OLED
    # i2cOLED.oled.invert(1)

    i2cOLED.oled.blit(fbuf, 0, 0)
    i2cOLED.oled.show()
    sleep(2)

def display_wifi():

    with open('WiFi_Logo.pbm', 'rb') as f:
        f.readline() # Magic number
        f.readline() # Creator comment
        f.readline() # Dimensions
        data = bytearray(f.read())
    fbuf = framebuf.FrameBuffer(data, 64, 38, framebuf.MONO_HLSB)
    # make sure, your image is inverted
    # if not, invert OLED
    # i2cOLED.oled.invert(1)

    i2cOLED.oled.blit(fbuf, 0, 0)
    i2cOLED.oled.show()
    sleep(2)
