import network
from time import sleep
import i2cOLED
import displayImage
from ntptime import settime
import machine
from cfg_wlan import *

def connect(useOled=True):
    i2cOLED.activate()
 
    station = network.WLAN(network.STA_IF)
 
    if station.isconnected() == True:
        print("Already connected")
        print()
        connectionInfo = station.ifconfig()
        print("IP: ", connectionInfo[0])
        print()
        return

    # display WiFi image or blank screen
    if useOled:
        displayImage.display_image("WiFi_Logo.pbm")
    else:
        i2cOLED.oled.fill(0)
        i2cOLED.oled.show()

    station.active(True)
    station.connect(wlan_ssid, wlan_password)
 
    while station.isconnected() == False:
        sleep(0.1)
        pass
    print()
    print("Connection successful!")
    print()
    connectionInfo = station.ifconfig()
    print("IP: ", connectionInfo[0])
    print()
    if useOled:
        i2cOLED.oled.text("WLAN",60,0)
        i2cOLED.oled.text("Connection", 60, 10)
        i2cOLED.oled.text("successful!", 60, 20)
        i2cOLED.oled.text(connectionInfo[0], 0, 50)
        i2cOLED.oled.show()

    # set UTC time
    # for testing: try with try/exception because of some errors
    # maybe this one: https://github.com/micropython/micropython/issues/4454
    # or this one: https://forum.micropython.org/viewtopic.php?f=2&t=5888&p=33684&hilit=settime#p33684
    if not machine.reset_cause() == machine.DEEPSLEEP_RESET:
        try:
            settime()
        except:
            print("There was an error, setting the time")

def disconnect(useOled=True):
    i2cOLED.activate()
    station = network.WLAN()
 
    if station.isconnected() == True:
        w = network.WLAN()
        w.disconnect()
        print("disconnect WLAN")
        print()
        if useOled:
            i2cOLED.oled.text("WLAN",0,0)
            i2cOLED.oled.text("disconnected", 00, 10)
            i2cOLED.oled.show()
        else:
            i2cOLED.oled.fill(0)
            i2cOLED.oled.show()
        return
