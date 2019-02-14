import i2cOLED
import framebuf
from time import sleep

def display_image(fileToDisplay, posX=0, posY=0):

    with open(fileToDisplay, 'rb') as f:
        f.readline() # Magic number
        f.readline()
        sizeX,sizeY = f.readline().split( ) # split by space
        data = bytearray(f.read())
    fbuf = framebuf.FrameBuffer(data, int(sizeX), int(sizeY), framebuf.MONO_HLSB)
    # make sure, your image is inverted
    # if not, invert OLED
    # i2cOLED.oled.invert(1)

    i2cOLED.oled.blit(fbuf, posX, posY)
    i2cOLED.oled.show()
    sleep(2)
