import i2cOLED
import connectWiFi
import machine

# reduce cpu speed
# will be added later

# activate OLED
i2cOLED.activate()

if not machine.reset_cause() == machine.DEEPSLEEP_RESET:
    import displayImage
    displayImage.display_image("BootLogo.pbm")

# connect to WiFi - is done later in mqtt_all
#connectWiFi.connect()

import mqtt_all


