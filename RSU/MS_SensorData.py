
# Import the necessary libraries

from __future__ import print_function
import paho.mqtt.client as mqtt
import Adafruit_DHT
import json
import time
import base64


def getSensorData():
    """
     Use the Adafruit_DHT library.It reads temperature and humidity from the DHT-22 sensor connected to Raspberry Pi 3.
     It assign them to either temperature or humidity variables and return them.
    :return: string value of humidity and temperature from the sensor.
    For more information refers to the Adafruit_DHT library.
    """
    HumR, TempR = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 18)
    RpiH = ("%.2f" % round(HumR, 2))
    RpiT = ("%.2f" % round(TempR, 2))
    return str(RpiH), str(RpiT)


def updateRpiSen():
    """
    Calls getSensorData at every given amount of time (updateInterval). Then calls the mqttSendStatusRSU() function to
    publish the data on the MQTT Broker following a certain format.
    :return:
    """
    global lastRpiUpdateTime
    if time.time() - lastRpiUpdateTime >= updateInterval:
        sen_hum, sen_temp = getSensorData()
        lastRpiUpdateTime = time.time()
        mqttSendStatusRSU(sen_temp, sen_hum)


def mqttSendStatusRSU(sen_temp, sen_hum):
    """
    This function publish a JSON format file on the MQTT Broker under the topic "/RSU/local/nameOfSensor/json".
    It precise the deviceID and all the data gathered by the local Sensor (Temperature, Humidity, units). A timestamp
    is added to the message.
    The QoS is 1, it is what OneM2M standard recommend.
    :param sen_temp:
    :param sen_hum:
    :return:
    """
    rsu_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(lastRpiUpdateTime))
    payload = ("""
    {
        "deviceID" : "Sensor3",
        "Data" :{
                    "Temperature" : {
                    "data": "%s",
                    "unit" : "C"
                    },
                    "Humidity" : {
                    "data" : "%s",
                    "unit" : "%%"
                    },
                    "Timestamp" : "%s"
                }
    }
    """%(sen_temp,sen_hum,rsu_time))
    client.publish("/RSU/local/Sensor3/json", payload, 1)

    f = open("Receive/Sensor.txt", "a+")
    f.write(payload + "\n")
    f.close()


def saveMqttData(msg):
    """
    from a message received from the MQTT Broker, this function retrieve either the data from the sensor (payload
    started with : app) or the timestamp (payload started with :rxI). To link those two information a comparison
    from the expected device to the effective device is done. To do so, the deviceName (application) and the phyPayload
    (gateway) are used. The mac address cannot be used because it is the one of the gateway and not the sensor.
    The data received from the application topic are encrypted and needs to be decrypted. Once decrypted, the data
    payload should looks like : Sensor1:35.7:C:64.9:%
    As the topic are publish in a certain order on the MQTT Broker :
    - gateway/+/rx
    - application/+/node/+/rx
    So, once the topic received is application, the timestamp is already record and the complete data can be published on
    the MQTT Broker. This is why the sendMQTTData() function is only call if the msg_payload is app.
    :param msg:
    :return:
    """
    global dev_id, Sensor1_time, Sensor2_time
    msg_payload = str(msg.payload)
    if msg_payload[2:5] == "app":
        parsed_json = json.loads(str(msg.payload))
        dev_id=parsed_json['deviceName']
        sen_reading=str(base64.b64decode(parsed_json['data'])).split(':',5)
        if dev_id == 'Sensor1':
               sendMQTTData(sen_reading, Sensor1_time)

        if dev_id == 'Sensor2':
               sendMQTTData(sen_reading, Sensor2_time)

    if msg_payload[2:5] == "rxI":
        parsed_json = json.loads(str(msg.payload))
        phyPayload=parsed_json['phyPayload']
        timestamp = parsed_json['rxInfo']['time']

        # Using the payload to establish to which sensor the timestamp belong
        if str(phyPayload)[:3] == "QAE":
            Sensor1_time = str(timestamp)

        # Using the payload to establish to which sensor the timestamp belong
        if str(phyPayload)[:3] == "QAI":
            Sensor2_time = str(timestamp)


def on_connect(client, userdata, flags, rc):
    """
    rc is the error code returned when connecting to the broker
    Once the client has connected to the broker, subscribe to the topic you are interested in.
    Here subscribes to mqtt topics of LoRa : - application for the data of the remote sensor.
                                             - gateway to get a timestamp for the data.
    :param client:
    :param userdata:
    :param flags:
    :param rc:
    :return:
    """
    client.subscribe(mqtt_topic_app)
    client.subscribe(mqtt_topic_gate)


def on_message(client, userdata, msg):
    """
    MQTT on message callback method.
    This function is called everytime the topic is published to.
    If you want to check each message, and do something depending on
    the content, the code to do this should be run in this function.
    Here everytime a message is received the saveMqttData() function is called to record the information.
    :param client:
    :param userdata:
    :param msg:
    :return:
    """
    saveMqttData(msg)


def sendMQTTData(sen_reading, timestamp):
    """
    This function publish a JSON format file on the MQTT Broker under the topic "/RSU/remote/nameOfSensor/json".
    It precise the deviceID and all the data gathered by the remote Sensor (Temperature, Humidity, Timestamp, units).
    The QoS is 1, it is what OneM2M standard recommend.
    Update the content of Sensor.txt
    :param sen_reading:
    :param timestamp:
    :return:
    """
    payload = ("""
    {
        "deviceID" : "%s",
        "Data" :{
                    "Temperature" : {
                    "data": "%s",
                    "unit" : "%s"
                    },
                    "Humidity" : {
                    "data" : "%s",
                    "unit" : "%s"
                    },
                    "Timestamp" : "%s"
                }
    }
    """%(sen_reading[0], sen_reading[1], sen_reading[2], sen_reading[3], sen_reading[4], timestamp))
    client.publish("/RSU/remote/{}/json".format(sen_reading[0]), payload, 1)

    f = open("Receive/Sensor.txt", "a+")
    f.write(payload + "\n")
    f.close()


def main():
    """
    main function initiate the MQTT related function and connect to the broker.
    It runs a while True loop with exception catcher to make sure that the
    loop will not stopped. Then, every 20 seconds, it reads the data from the Sensor and send it to the MQTT Broker.
    :return:
    """
    try:
        client.on_connect = on_connect
        client.on_message = on_message
        # Once everything has been set up, we can connect to the broker
        # 1883 is the listener port that the MQTT broker is using
        client.connect(mqtt_broker_ip, 1883)
        client.loop_start()
        while True:
            updateRpiSen()
            time.sleep(20)
    except (KeyboardInterrupt, SystemExit):
        print("\nKilling Thread...")
        client.disconnect()
    print("Done.\nExiting.")


if __name__ == '__main__':
    # MQTT
    mqtt_username = "loraroot"
    mqtt_password = "root"
    mqtt_topic_app = "application/+/node/+/rx"
    mqtt_topic_gate = "gateway/+/rx"
    mqtt_broker_ip = "localhost"
    client = mqtt.Client()

    # Track the last Rpi update time
    lastRpiUpdateTime = time.time()

    # Update once every 15 seconds
    updateInterval = 15

    # Set the username and password for the MQTT client
    client.username_pw_set(mqtt_username, mqtt_password)
    # call main function
    main()
