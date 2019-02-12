from time import sleep
import dht
import machine
import i2cOLED

def values():
    i2cOLED.activate()

    sensor = dht.DHT22(machine.Pin(17))

    for I in range(5):

        sensor.measure()
        #sensor.temperature()
        #sensor.humidity()

        t = sensor.temperature()
        h = sensor.humidity()
        print("Temperatur:  ", t, "*C")
        print("Luftfeuchte: ", h, "%")
        print("-----------")
        i2cOLED.oled.fill(0)
        i2cOLED.oled.show()
        tText = 'T: ' + str(sensor.temperature())
        i2cOLED.oled.text(tText, 0, 0)

        hText = 'H: ' + str(sensor.humidity())
        i2cOLED.oled.text(hText, 0, 30)

        # graphics.line(0, 0, 127, 63, 1)

        # graphics.rect(8,50,112,12,1)
        # graphics.rect(8,20,112,12,1)

        i2cOLED.graphics.rect(8, 50, 112, 12, 1)
        i2cOLED.graphics.fill_rect(8, 50, int(h/100*112), 12, 1)
        i2cOLED.oled.show()

        I += I
        #machine.deepsleep(5000)
        sleep(5)

