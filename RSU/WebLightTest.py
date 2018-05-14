import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import thingspeak
import time

GPIO.setmode(GPIO.BCM)
GreenLight = 5
RedLight = 13
BlueLight = 6
GPIO.setup(GreenLight, GPIO.OUT, initial=0)
GPIO.setup(RedLight, GPIO.OUT, initial=0)
GPIO.setup(BlueLight, GPIO.OUT, initial=0)
turnedOnRed = False
turnedOnGreen = False
turnedOnBlue = False

channel_id = "472117"
write_key = "YIWBEMNVPZ1XKN6Z"

channel = thingspeak.Channel(id=channel_id, write_key=write_key)

# MQTT
mqtt_username = "loraroot"
mqtt_password = "root"
mqtt_broker_ip = "localhost"
client = mqtt.Client()
mqtt_Light_topic = "light/#"
cloud_topic = "channels/472117/subscribe/fields/field2/EYNVO9MB25DIYJFQ"


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
    client.subscribe(mqtt_Light_topic)


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
    sortLight(msg)


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
        # print(message)
        time.sleep(15)
        response = channel.update({message[0]: message[1], message[2]: message[3]})
        print(response)
    except:
        print("connection failed")


def sortLight(msg):
    global turnedOnBlue, turnedOnGreen, turnedOnRed
    print(msg.topic)
    if msg.topic == "light/RED":
        turnedOnRed = changelight(turnedOnRed, RedLight)
        if turnedOnRed:
            status = "On"
        else:
            status = "Off"
        payload = ("""{"color" : "Red",
        "lightStatus" : "%s",
        "payload" : "This is a payload to test message received"}"""% status)
        message = [2, payload, 3, str(72)]
        postThingspeak(message)
        client.publish(cloud_topic, payload)
    if msg.topic == "light/GREEN":
        turnedOnGreen = changelight(turnedOnGreen, GreenLight)
        if turnedOnGreen:
            status = "On"
        else:
            status = "Off"
        payload = ("""{"color" : "Green",
        "lightStatus" : "%s",
        "payload" : "This is a payload to test message received"}"""% status)
        message = [2, payload, 3, str(73)]
        postThingspeak(message)
        client.publish(cloud_topic, payload)
    if msg.topic == "light/BLUE":
        turnedOnBlue = changelight(turnedOnBlue, BlueLight)
        if turnedOnBlue:
            status = "On"
        else:
            status = "Off"
        payload = ("""{"color" : "Blue",
        "lightStatus" : "%s",
        "payload" : "This is a payload to test message received"}"""% status)
        message = [2, payload, 3, str(74)]
        postThingspeak(message)
        client.publish(cloud_topic, payload)


def changelight(turnedOn, LightOn):
    if turnedOn:
        GPIO.output(LightOn, GPIO.LOW)
        turnedOn = False
    else:
        GPIO.output(LightOn, GPIO.HIGH)
        turnedOn = True
    return turnedOn


def main():
    try:
        client.on_connect = on_connect
        client.on_message = on_message
        # Once everything has been set up, we can (finally) connect to the broker
        # 1883 is the listener port that the MQTT broker is using
        client.connect(mqtt_broker_ip, 1883)
        client.loop_forever()
    except (KeyboardInterrupt, SystemExit):  # when you press ctrl+c
        print("\nKilling Thread...")
        GPIO.output(RedLight, GPIO.LOW)
        GPIO.output(GreenLight, GPIO.LOW)
        GPIO.output(BlueLight, GPIO.LOW)
        client.disconnect()
    print("Done.\nExiting.")


if __name__ == '__main__':
    main()