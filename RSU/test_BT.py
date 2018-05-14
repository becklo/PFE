import bluetooth
import time
import paho.mqtt.client as mqtt

deviceList = [["b8:27:eb:4b:da:38", "raspberrypi"], ["A8:5c:2c:3a:fc:e0", "iPhone de Loula Beck"]]
# , ["24:0a:c4:02:5c:aa", "LoPy"]]
# , ["20:16:d8:9e:f2:38", "LUBTZLLBECK"]]

# MQTT
mqtt_username = "loraroot"
mqtt_password = "root"
mqtt_broker_ip = "localhost"
client = mqtt.Client()

# Set the username and password for the MQTT client
client.username_pw_set(mqtt_username, mqtt_password)


def on_connect(client, userdata, flags, rc):
    """
    rc is the error code returned when connecting to the broker
    Once the client has connected to the broker, subscribe to the topic you are interested in.
    :param client:
    :param userdata:
    :param flags:
    :param rc:
    :return:
    """
    print("On Connect")


def on_message(client, userdata, msg):
    """
    MQTT on message callback method.
    This function is called everytime the topic is published to.
    If you want to check each message, and do something depending on
    the content, the code to do this should be run in this function
    :param client:
    :param userdata:
    :param msg:
    :return:
    """
    print("On Message")


def sendMQTTData(device):
    """
    This function publish a JSON format file on the MQTT Broker under the topic "/RSU/local/BLE/json".
    It precise the deviceID and that an authentication was made at a precise timestamp. It is a Boolean for now
    but it could be the mac address of the device.
    The QoS is 1, it is what OneM2M standard recommend.
    Update the content of the BLE.txt file.
    :param authenticate
    :return:
    """
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()))
    payload = ("""
    {
        "deviceID" : "BLE",
        "Data" :{
                    "Device" : "%s",
                    "timestamp" : "%s"
                }
    }
    """ % (device, timestamp))
    client.publish("/RSU/local/BLE/json", payload, 1)

    f = open("Receive/BLE.txt", "a+")
    f.write(payload + "\n")
    f.close()


client.on_connect = on_connect
client.on_message = on_message
# Once everything has been set up, we can (finally) connect to the broker
# 1883 is the listener port that the MQTT broker is using
client.connect(mqtt_broker_ip, 1883)
client.loop_start()

while 1:
    authentication = False

    for i in range(len(deviceList)):
        if bluetooth.lookup_name(deviceList[i][0]) == deviceList[i][1]:
            print(deviceList[i][1] + " authentication succeeded")
            sendMQTTData(deviceList[i][0])
            timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()))
            print("time : " + timestamp)
            authentication = True
            time.sleep(3)
        i+=1

    if not authentication:
        print("no authorized devices near")
    time.sleep(3)
