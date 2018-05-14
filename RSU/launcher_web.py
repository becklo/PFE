
import paho.mqtt.client as mqtt
import thingspeak
import time
import os


def on_connect(client, userdata, flags, rc):
    """
    rc is the error code returned when connecting to the broker
    Once the client has connected to the broker, subscribe to the topic you are interested in.
    Here all topics from ThinspeakSubscribe.py
    :param client:
    :param userdata:
    :param flags:
    :param rc:
    :return:
    """
    client.subscribe(mqtt_Control_topic)
    print("connected")


def on_message(client, userdata, msg):
    """
    MQTT on message callback method.
    This function is called everytime the topic is published to. If you want to check each message, and do something
    depending on the content, the code to do this should be run in this function.
    Here call the sortCommand() function.
    :param client:
    :param userdata:
    :param msg:
    :return:
    """
    sortCommand(msg)


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
        time.sleep(15)
        response = channel.update({message[0]: message[1], message[2]: message[3]})
        print(response)
    except:
        print("connection failed")


def killService(name):
    """
    This function kill with option -15 so it can terminate its action before beeing killed. It uses the pkill -f command
    to be able to kill a service with its name only. The list of services running is then updated.
    A status uptade is published to the MQTT broker on a topic similar to Thingspeak's ones so the web interface can
    process it.
    :param name:
    :return:
    """
    f = open("Receive/serviceList.txt", "a+")
    serviceList = f.readlines()
    f.close()
    print(serviceList)
    for i in serviceList:
        if i == "\n":
            serviceList.remove(i)
    print(serviceList)
    if name + "\n" in serviceList:
        command = "sudo pkill -15 -f " + name
        print(command)
        os.system(command)
        f = open("Receive/serviceList.txt", "w")
        serviceList.remove(name + "\n")
        print(serviceList)
        for line in serviceList:
                f.write(line + "\n")
        f.close()
        print(serviceList)
        test = "Stopped"
    else:
        print("service already not running")
        print("Here are the services running : ")
        print(serviceList)
        test = "service already not running"
    # f.close()
    nameCleaned = name.replace("MS_", "")
    nameCleaned = nameCleaned.replace(".py", "")
    print("Publishing data from " + nameCleaned)
    publishData(nameCleaned, "Off", test)


def start_service(name):
    """
    Check if the service is not already running (in serviceList), if not it is started.
    A status update is published to the MQTT broker so the web interface can process it.
    :param name:
    :return:
    """
    f = open("Receive/serviceList.txt", "a+")
    serviceList = f.readlines()
    f.close()
    print(serviceList)
    if not name + "\n" in serviceList:
        f = open("Receive/serviceList.txt", "a+")
        f.write(name + "\n")
        f.close()
        command = "sudo python " + name + " &"
        print(command)
        os.system(command)
        test = "Started"
    else:
        print("Service already running")
        test = "Service already running"
    print(serviceList)
    nameCleaned = name.replace("MS_", "")
    nameCleaned = nameCleaned.replace(".py", "")
    print("Publishing data from " + nameCleaned)
    publishData(nameCleaned, "On", test)


def publishData(name, status, data):
    """
    Publish a json file to the local MQTT broker under a topic similar to thingspeak (Web interface can't subscribe to
    the cloud so this pretend it does)
    :param name:
    :param status:
    :param data:
    :return:
    """
    payload = ("""
    {
        "serviceTest" : "%s",
        "serviceStatus" : "%s",
        "payload" : "%s"
    }
    """ % (name, status, data))
    client.publish(cloud_topic, payload)


def sortCommand(msg):
    """
    Depending on the topic, either the start or stop service function is called.
    :param msg:
    :return:
    """
    print(msg.topic)
    if msg.topic == "Control/start/Truck":
        start_service("MS_Traffic.py")
    if msg.topic == "Control/start/Cloud":
        start_service("MS_Cloud.py")
    if msg.topic == "Control/start/Weather":
        start_service("MS_Weather.py")
    if msg.topic == "Control/start/GPS":
        start_service("MS_GPS.py")
    if msg.topic == "Control/start/Sensor":
        start_service("MS_SensorData.py")
    if msg.topic == "Control/start/BLE":
        start_service("MS_BLE.py")
    if msg.topic == "Control/start/Translator":
        start_service("sh ./../Controller.sh")
        time.sleep(30)
        start_service('MS_Translator.py')
    if msg.topic == "Control/start/All":
        start_service("sh ./../Controller.sh")
        time.sleep(30)
        start_service('MS_Translator.py')
        time.sleep(20)
        start_service("MS_Traffic.py")
        start_service("MS_Cloud.py")
        start_service("MS_Weather.py")
        start_service("MS_GPS.py")
        start_service("MS_SensorData.py")
        start_service("MS_BLE.py")
    if msg.topic == "Control/stop/Truck":
        killService("MS_Traffic.py")
    if msg.topic == "Control/stop/Cloud":
        killService("MS_Cloud.py")
    if msg.topic == "Control/stop/Weather":
        killService("MS_Weather.py")
    if msg.topic == "Control/stop/GPS":
        killService("MS_GPS.py")
    if msg.topic == "Control/stop/Sensor":
        killService("MS_SensorData.py")
    if msg.topic == "Control/stop/BLE":
        killService("MS_BLE.py")
    if msg.topic == "Control/stop/Translator":
        os.system("sudo killall -15 java")
        os.system("echo")
        killService('MS_Translator.py')
    if msg.topic == "Control/stop/All":
        f = open("Receive/serviceList.txt", "r")
        serviceList = f.readlines()
        f.close()
        for name in serviceList:
            if name == "Translator.py":
                os.system("sudo killall -15 java")
                os.system("echo")
            killService(name)


def main():
    """
     It runs with exception catcher to make sure that the if an exception is catched it will be disconnected from the
    MQTT Broker.
    Initiate the MQTT related function.
    :return:
    """
    try:
        client.on_connect = on_connect
        client.on_message = on_message
        # Once everything has been set up, we can (finally) connect to the broker
        # 1883 is the listener port that the MQTT broker is using
        client.connect(mqtt_broker_ip, 1883)
        client.loop_forever()
    except (KeyboardInterrupt, SystemExit):  # when you press ctrl+c
        print("\nKilling Thread...")
        client.disconnect()
        # os.system("sudo killall -15 java")
        # os.system("echo")
        # kill all microservices
        # os.system("sudo killall -15 python")
    print("Done.\nExiting.")


if __name__ == '__main__':
    # Thingspeak related info
    channel_id = "472117"
    write_key = "YIWBEMNVPZ1XKN6Z"

    channel = thingspeak.Channel(id=channel_id, write_key=write_key)

    # MQTT
    mqtt_username = "loraroot"
    mqtt_password = "root"
    mqtt_broker_ip = "localhost"
    client = mqtt.Client()
    mqtt_Control_topic = "Control/#"
    cloud_topic = "channels/472117/subscribe/fields/field2/EYNVO9MB25DIYJFQ"

    # Set the username and password for the MQTT client
    client.username_pw_set(mqtt_username, mqtt_password)
    main()