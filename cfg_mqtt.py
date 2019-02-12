""" ##### MQTT ##### """

""" MQTT Thingspeak Variables """
thingspeakUserId = b"YourThingspeakUserID"  # EDIT - enter Thingspeak User ID
thingspeakMqttApiKey = b"YourThingspeakMQTTAPIKey"  # EDIT - enter Thingspeak MQTT API Key
thingspeakChannelId = b"YourThingspeakChannelID"  # EDIT - enter Thingspeak Channel ID
thingspeakChannelWriteApiKey = b"YourThingspeakWriteAPIKey"  # EDIT - enter Thingspeak Write API Key

""" MQTT Hiveeyes Variables """
# MQTT hiveeyes topic
mqtt_topic_hiveeyes = u'{realm}/{network}/{gateway}/{node}/data.json'.format(
    realm   = 'hiveeyes',
    network = 'testdrive',
    gateway = 'garten',
    node    = 'waage1'
)

""" MQTT URLs """
thingspeakUrl = b"mqtt.thingspeak.com"
hiveeyesUrl = 'swarm.hiveeyes.org'

# unique client-id, created with:
# python3 -c 'from uuid import uuid4; print(uuid4())'
MqttClientID = 'your-uuid-here'





