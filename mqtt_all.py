#from umqtt.robust import MQTTClient   # Which is better? simple or robust?
from umqtt.simple import MQTTClient
import os
import ujson   # normal Python uses json
import network
from dht import DHT22
from time import sleep
import machine
import connectWiFi
import gc
from cfg_mqtt import * # config file
import sys
from hx711lib import HX711
import connectWiFi

sensor = DHT22(machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_UP))

# special wiring on the chinese HX711
# E+ = white
# E- = black
# A- = red
# A+ = green
# normally it is E+ = red and A- = white

# sck  = 2
# dout = 0
sc = HX711(0,2)

publishPeriodInSec = 355 # 360s minus 5s sleep time, so almost 5 min

# give time to publish new main.py if needed, because ESP32 is going to deepsleep later
# and you don't have enough time if something goes wrong
sleep(4)

def hiveeyes_publish(t, h, w):
    measurement = {
                'temperature0': t,
                'humidity': h,
                'weight': w
            }

    # Serialize data as JSON
    hiveeyes_payload = ujson.dumps(measurement)
    # Publish to MQTT
    client_hiveeyes = MQTTClient(client_id=MqttClientID, server=hiveeyesUrl, user='Your@Mail.adr', password='YourPassword', ssl=False)
    client_hiveeyes.connect()
    client_hiveeyes.publish(mqtt_topic_hiveeyes, hiveeyes_payload)
    client_hiveeyes.disconnect()


def thingspeak_publish(t, h, w):
    #
    # connect to Thingspeak MQTT broker
    # connection uses unsecure TCP (port 1883)
    #
    # To use a secure connection (encrypted) with TLS:
    #   set MQTTClient initializer parameter to "ssl=True"
    #   Caveat: a secure connection uses about 9k bytes of the heap
    #         (about 1/4 of the micropython heap on the ESP8266 platform)
    thingspeak_client = MQTTClient(client_id=MqttClientID,
                        server=thingspeakUrl,
                        user=thingspeakUserId,
                        password=thingspeakMqttApiKey,
                        ssl=False)
    thingspeak_client.connect()
    credentials = bytes("channels/{:s}/publish/{:s}".format(thingspeakChannelId, thingspeakChannelWriteApiKey), 'utf-8')
    thingspeak_payload = "field1="+str(t)+"&field2="+str(h)+"&field3="+str(w)
    thingspeak_client.publish(credentials, thingspeak_payload)
    thingspeak_client.disconnect()

while True:
    sensor.measure()   # Poll sensor
    t, h, w = sensor.temperature(), sensor.humidity(), sc.get_kg()
    print('T:' + str(t) + '*C')
    print('H:' + str(h) + '%')
    print('W:' + str(w) + 'kg')

    if all(isinstance(i, float) for i in [t, h, w]):   # Confirm values and send

        station = network.WLAN(network.STA_IF)
        # connect to WiFi
        connectWiFi.connect(useOled=True)

        if not station.isconnected():
            print("WLAN not connected!")
            print("Exit here")
            sys.exit()

        try:
            thingspeak_publish(t, h, w)
        except:
            print('error while uploading to thingspeak')

        try:
            hiveeyes_publish(t ,h, w)
        except:
            print('error while uploading to hiveeyes')

        connectWiFi.disconnect()

        # 1 sec sleep to display "WLAN disconnected" on OLED
        print('going to sleep...')
        sleep(1)

        # clearing up
        gc.collect()
        gc.mem_free()

        print('going to deepsleep...')
        #machine.deepsleep(publishPeriodInSec * 1000) # real use
        sleep(15) # testing

    else:
        print('Invalid reading ... tryins again in 5s ...')
        sleep(5)
