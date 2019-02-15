import machine
import ssd1306
from time import sleep
import gfx
import framebuf

def activate():

    # set Pins
    sclPin = machine.Pin(15)
    sdaPin = machine.Pin(4)
    rstPin = machine.Pin(16, machine.Pin.OUT)

    # set width and height
    oledWidth = 128
    oledHeight = 64

    # set RST to high
    # https://forum.micropython.org/viewtopic.php?t=4002
    rstPin.value(1)

    # initialize Display
    i2c = machine.I2C(scl=sclPin, sda=sdaPin)
    
    global oled
    oled = ssd1306.SSD1306_I2C(oledWidth, oledHeight, i2c)
    global graphics
    graphics = gfx.GFX(oledWidth, oledHeight, oled.pixel)

    # OLED schwarz und wenig Kontrast
    # oled.contrast(0) wenig <--> oled.contrast(255) max
    oled.contrast(0)
    oled.fill(0)
    oled.show()

    # graphics = gfx.GFX(oledWidth, oledHeight, oled.pixel)
    # graphics.line(0, 0, 127, 63, 1)
    #
    # graphics.rect(8,50,112,12,1)
    # graphics.fill_rect(8,20,112,12,1)
