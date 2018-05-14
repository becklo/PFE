# Import the necessary libraries

from __future__ import print_function

import json

import paho.mqtt.client as mqtt
import time
import random


def on_connect_TS(client, userdata, flags, rc):
    """
    rc is the error code returned when connecting to the broker
    Once the client has connected to the broker, subscribe to the topic you are interested in.
    Here the topic from the thingspeak Broker.
    :param client:
    :param userdata:
    :param flags:
    :param rc:
    :return:
    """
    clientTS.subscribe(thingspeak_topic)
    print("On Connect TS")


def on_message_TS(client, userdata, msg):
    """
    MQTT on message callback method.
    This function is called everytime the topic is published to. If you want to check each message, and do something
    depending on the content, the code to do this should be run in this function
    Here, sort depending on the field that is updated :
    - 1 : calls sendMQTTData() function to publish a topic corresponding to the code sent
    - 4 : update database with form information
    :param client:
    :param userdata:
    :param msg:
    :return:
    """
    global clientList
    print("On Message TS")
    # print(msg.payload)
    # print(msg.topic)
    # timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()))
    # print(timestamp)
    if msg.topic == "channels/472117/subscribe/fields/field1/EYNVO9MB25DIYJFQ":
        sendMQTTData(msg.payload)
    elif msg.topic == "channels/472117/subscribe/fields/field4/EYNVO9MB25DIYJFQ":
        print(msg.payload)
        message = json.loads(str(msg.payload))
        carId = message['carId']
        if carId in clientList:
            f = open("MicroServices/DataBase.json", "r")
            lines = f.readlines()
            f.close()
            f = open("MicroServices/DataBase.json", "w+")
            for line in lines:
                if line[:14] != "{\"carId\" : \"" + carId + "\"":
                    f.write(line)
        else:
            clientList += carId
        f = open("MicroServices/DataBase.json", "a+")
        f.write(msg.payload + "\n")
        f.close()


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
    print("On Connect Local")


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
    print("On Message Local")


def sendMQTTData(msg):
    """
    Depending on the payload received publish a given topic so the launcher_web.py can start or stop the specified topic
    :param msg:
    :return:
    """
    print(msg)
    if str(msg) == "72":
        client.publish("light/RED", "hello", 1)
    if str(msg) == "73":
        client.publish("light/GREEN", "hello", 1)
    if str(msg) == "74":
        client.publish("light/BLUE", "hello", 1)
    if str(msg) == "100":
        client.publish("Control/start/Truck", "hello", 1)
    if str(msg) == "101":
        client.publish("Control/start/Cloud", "hello", 1)
    if str(msg) == "102":
        client.publish("Control/start/Weather", "hello", 1)
    if str(msg) == "103":
        client.publish("Control/start/GPS", "hello", 1)
    if str(msg) == "104":
        client.publish("Control/start/Sensor", "hello", 1)
    if str(msg) == "105":
        client.publish("Control/start/BLE", "hello", 1)
    if str(msg) == "106":
        client.publish("Control/start/Translator", "hello", 1)
    if str(msg) == "109":
        client.publish("Control/start/All", "hello", 1)
    if str(msg) == "200":
        client.publish("Control/stop/Truck", "hello", 1)
    if str(msg) == "201":
        client.publish("Control/stop/Cloud", "hello", 1)
    if str(msg) == "202":
        client.publish("Control/stop/Weather", "hello", 1)
    if str(msg) == "203":
        client.publish("Control/stop/GPS", "hello", 1)
    if str(msg) == "204":
        client.publish("Control/stop/Sensor", "hello", 1)
    if str(msg) == "205":
        client.publish("Control/stop/BLE", "hello", 1)
    if str(msg) == "206":
        client.publish("Control/stop/Translator", "hello", 1)
    if str(msg) == "209":
        client.publish("Control/stop/All", "hello", 1)


def main():
    """
    main function initiate the MQTT related function and connect to the broker.
    It runs a while True loop with exception catcher to make sure that the
    loop will not stopped.
    On exception disconnect from both mqtt brokers.
    :return:
    """
    try:
        clientTS.on_connect = on_connect_TS
        clientTS.on_message = on_message_TS
        client.on_connect = on_connect
        client.on_message = on_message
        # Once everything has been set up, we can (finally) connect to the broker
        # 1883 is the listener port that the MQTT broker is using
        clientTS.connect(mqtt_broker_ip_TS, 1883)
        clientTS.loop_start()
        client.connect(mqtt_broker_ip, 1883)
        client.loop_start()
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        print("\nKilling Thread...")
        clientTS.disconnect()
        client.disconnect()
    print("Done.\nExiting.")


if __name__ == '__main__':
    # MQTT
    mqtt_username_TS = "loulabecksesco"
    mqtt_password_TS = "D8ZQSQ59YDSSLDBE"
    mqtt_broker_ip_TS = "mqtt.thingspeak.com"
    thingspeak_topic = "channels/472117/subscribe/fields/+/EYNVO9MB25DIYJFQ"

    clientTS = mqtt.Client()

    # Set the username and password for the MQTT client
    clientTS.username_pw_set(mqtt_username_TS, mqtt_password_TS)

    # MQTT
    mqtt_username = "loraroot"
    mqtt_password = "root"
    mqtt_broker_ip = "localhost"
    client = mqtt.Client()

    # Set the username and password for the MQTT client
    client.username_pw_set(mqtt_username, mqtt_password)

    clientList = []

    # call main function
    main()


