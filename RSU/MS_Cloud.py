# Import the necessary libraries

from __future__ import print_function
import paho.mqtt.client as mqtt
import json
import thingspeak


def on_connect(client, userdata, flags, rc):
    """
    rc is the error code returned when connecting to the broker
    Once the client has connected to the broker, subscribe to the topic you are interested in.
    Here subscribes to mqtt topics of the sensors
    :param client:
    :param userdata:
    :param flags:
    :param rc:
    :return:
    """
    client.subscribe(mqtt_topic_remote)
    client.subscribe(mqtt_topic_local)


def on_message(client, userdata, msg):
    """
    MQTT on message callback method.
    This function is called every time the topic is published to.
    If you want to check each message, and do something depending on
    the content, the code to do this should be run in this function.
    Here, if the topic is relevant, call updateCloud()
    :param client:
    :param userdata:
    :param msg:
    :return:
    """
    if msg.topic == "/RSU/local/Sensor3/json" or msg.topic == "/RSU/remote/Sensor1/json" \
            or msg.topic == "/RSU/remote/Sensor2/json":
        updateCloud(msg)


def postThingspeak(message):
    """
    Call to send messages to the Cloud. This function calls a function from the Thingspeak library. To install it :
    pip install thingspeak
    The channel must be set, to do so please add the channel_id and write_key at the beginning of the program.
    The Cloud seems to be able to keep up without sleep. If problems with the Cloud appears, set a time.sleep().
    The arguments of the called function are :
     channel.update(field : data, field :data), find more information in thingspeak library docs.
    :param message:
    :return:
    """
    try:
        response = channel.update({message[0]: message[1], message[2]: message[3]})
        # time.sleep(10)
        print(response)
    except:
        print("connection failed")


def updateCloud(msg):
    """
    Call when messages are published on /RSU/+/+/json from sensors. It parsed the information from the JSON received
    and send it to Thingspeak Cloud. The field where the information is send depends on the sensor form where it comes.
    The Timestamp is not taking ino account because it cannot be send to the Cloud. Only the Temperature and the
    Humidity are processed.
    :param msg:
    :return:
    """
    parsed_json = json.loads(str(msg.payload))
    # temperature and Humidity define on ThingSpeak
    temp = parsed_json['Data']["Temperature"]['data']
    hum = parsed_json['Data']["Humidity"]['data']

    if msg.topic == "/RSU/remote/Sensor1/json":
        message = [1, temp, 2, hum]
        postThingspeak(message)

    if msg.topic == "/RSU/remote/Sensor2/json":
        message = [3, temp, 4, hum]
        postThingspeak(message)

    if msg.topic == "/RSU/local/Sensor3/json":
        message = [5, temp, 6, hum]
        postThingspeak(message)


def main():
    """
    main function. Initiate the MQTT related function. Has exception to be able to disconnect from the MQTT Broker.
    :return:
    """
    try:
        client.on_connect = on_connect
        client.on_message = on_message
        # Once everything has been set up, we can connect to the broker
        # 1883 is the listener port that the MQTT broker is using
        client.connect(mqtt_broker_ip, 1883)
        client.loop_forever()
    except (KeyboardInterrupt, SystemExit):  # when you press ctrl+c
        print("\nKilling Thread...")
        client.disconnect()
        print("Done.\nExiting.")


if __name__ == '__main__':
    channel_id = "435527"
    write_key = "DC38V8KV4P8Z0JYC"

    channel = thingspeak.Channel(id=channel_id, write_key=write_key)

    # MQTT
    mqtt_username = "loraroot"
    mqtt_password = "root"
    mqtt_topic_remote = "/RSU/remote/+/json"
    mqtt_topic_local = "/RSU/local/+/json"
    mqtt_broker_ip = "localhost"
    client = mqtt.Client()

    # Set the username and password for the MQTT client
    client.username_pw_set(mqtt_username, mqtt_password)
    # call main function
    main()
