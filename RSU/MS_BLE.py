
# Import the necessary libraries

from __future__ import print_function
from bluepy.btle import Scanner, DefaultDelegate, Peripheral, BTLEException
import paho.mqtt.client as mqtt
import time


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


def sendMQTTData(authenticate):
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
                    "Device" : "24:0a:c4:02:5c:aa",
                    "Authentication" : "%s",
                    "unit" : "Boolean",
                    "timestamp" : "%s"
                }
    }
    """ % (authenticate, timestamp))
    client.publish("/RSU/local/BLE/json", payload, 1)

    f = open("Receive/BLE.txt", "a+")
    f.write(payload + "\n")
    f.close()

class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
        """
        Here you should define the function to do when the connection is established, is this case sendMQTTData()
        :param cHandle:
        :param data:
        :return:
        """
        global authStatus
        # ... perhaps check cHandle
        # ... process 'data'.
        auth = str(data)
        authStatus = auth
        if isConnected:
            sendMQTTData(True)


def initBLE():
    """
    Initialisation of BLE
    connects with BLE device, sets Delegate, gets Services and Characteristics from BLE device.
    If a connection to an authenticated device is done, isConnected become true else it stay false.
    :return:
    """
    global isConnected
    try:
        p.connect(authDevice)
        p.setDelegate(MyDelegate())
        isConnected=True
        # Setup to turn notifications on, e.g.
        # svc = p.getServiceByUUID(service_uuid)
        # ch = svc.getCharacteristics(char_uuid)[0]
    except BTLEException as e:
        # catch BTLEException ..disconnect from the device and start again
        isConnected = False
        p.disconnect()
        if e == "Device disconnected":
            isConnected = False


def startScan():
    """
    Starts BLE scan, if known device is found, it calls initBLE method.
    :return:
    """
    devices = scanner.scan(2)
    if not isConnected:
        for dev in devices:
            if (dev.addr == authDevice) and (not isConnected):
                initBLE()


def main():
    """
    It runs a while True loop with exception catcher to make sure that the
    loop will not stopped. Initiate the MQTT related function.
    Has exception to be able to disconnect from the MQTT Broker.
    :return:
    """
    global isConnected
    try:
        client.on_connect = on_connect
        client.on_message = on_message
        # Once everything has been set up, we can (finally) connect to the broker
        # 1883 is the listener port that the MQTT broker is using
        client.connect(mqtt_broker_ip, 1883)
        client.loop_start()
        while True:
            try:
                startScan()
                if isConnected:
                    if p.waitForNotifications(1.0):
                        # handleNotification() was called
                        continue
                else:
                    isConnected = False
                    startScan()
            except BTLEException as e:
                # catch BTLEException ..disconnect from the device and start again
                isConnected = False
                p.disconnect()
                if e == "Device disconnected":
                    isConnected = False
    except (KeyboardInterrupt, SystemExit):  # when you press ctrl+c
        print("\nKilling Thread...")
        client.disconnect()
    print("Done.\nExiting.")


if __name__ == '__main__':
    # BLE
    # authDevice = "A8:5c:2c:3a:fc:e0"  # My iPhone
    # device mac address
    authDevice = "24:0a:c4:02:5c:aa" # LoPy
    # authDevice = "b8:27:eb:4b:da:38" # My RPI3
    # Refere to : lopy (ble device) main.py
    # service_uuid = "00001000-0000-1000-8000-00805f9b34fb"
    # service_uuid = 0x001
    # Refere to : lopy (ble device) main.py
    # char_uuid = 0x002
    isConnected = False
    p = Peripheral()
    scanner = Scanner()
    authentificationTime = time.time()
    authStatus = ""

    # MQTT
    mqtt_username = "loraroot"
    mqtt_password = "root"
    mqtt_broker_ip = "localhost"
    client = mqtt.Client()

    # Set the username and password for the MQTT client
    client.username_pw_set(mqtt_username, mqtt_password)
    # call main function
    main()
