import os

import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time
import logging
import json
from calendar import timegm


def on_connect(client, userdata, flags, rc):
    """
    rc is the error code returned when connecting to the broker
    Once the client has connected to the broker, subscribe to the topic you are interested in.
    Here the BLE topic from MS_BLE.py
    :param client:
    :param userdata:
    :param flags:
    :param rc:
    :return:
    """
    client.subscribe(mqtt_BLE_topic)


def on_message(client, userdata, msg):
    global deviceList
    """
    MQTT on message callback method.
    This function is called everytime the topic is published to. If you want to check each message, and do something 
    depending on the content, the code to do this should be run in this function.
    In this case, this function check if the device detected has already been detected and if so for how long. If it 
    has never been seen or for too long, it updates a log file with the mac address of the device with a timestamp and
    calls the authentication() function.
    :param client:
    :param userdata:
    :param msg:
    :return:
    """
    parsed_JSON =json.loads(str(msg.payload))
    device = parsed_JSON['Data']['Device']
    if device == "b8:27:eb:4b:da:38": # raspberry pi
        idCar = 1
    elif device == "A8:5c:2c:3a:fc:e0": # my iPhone
        idCar = 2
    presence = False

    for i in range(len(deviceList)):
        if deviceList[i][0] == device:
            presence = True
            index = i

    if not presence:
        timestamp = parsed_JSON['Data']['timestamp']
        deviceList.append([device, timestamp])
        authentication(idCar)
        logging.info("First connection of " + str(device) + " at " + str(timestamp))

    else:
        timeDev = deviceList[index][1]
        timestamp = timegm(
                time.strptime(
                    timeDev.replace('Z', 'GMT'),
                    '%Y-%m-%dT%H:%M:%S%Z'
                )
            )
        if (time.time()-timestamp) > 30:
            authentication(idCar)
            deviceList[index][1] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()))
            logging.info("Reconnection of " + str(device) + " at " + str(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()))))


def authentication(idCar):
    """
    Change the lights color for a given period of time and call the sendDataToCar() function with  (for now) the IP
    address of the only car there is.
    :return:
    """
    GPIO.output(BLEAuthenOk, GPIO.HIGH)
    GPIO.output(BLEAuthenNotOk, GPIO.LOW)
    sendDataToCar("192.168.0.106", idCar)
    time.sleep(5)
    GPIO.output(BLEAuthenOk, GPIO.LOW)
    GPIO.output(BLEAuthenNotOk, GPIO.HIGH)


def readingJSON(idCar):
    """
    This function read the DataBase.json file to find the interests and put it into a string that can be used in an ssh
    command.
    :return: fileList : a list of all files required
    """
    fileList = ""
    f = open("DataBase.json", "r+")
    files = f.readlines()
    f.close()
    print(files)
    for line in files:
        if line[:14] == "{\"carId\" : \"" + str(idCar) + "\"":
            parsed_json = json.loads(str(line))
            interest = parsed_json["interest"]
            for i in interest:
                if i == "Parking":
                    parkingName = parsed_json["ParkingName"]
                    fileList += "Receive/" + parkingName + "*.txt "
                elif i == "Traffic" or i == "Sensor":
                    fileList += "Receive/" + i + "*.txt "
                elif i == "GPS" or i == "Weather":
                    fileList += "Receive/" + i + ".txt "
            print(fileList)
            return fileList


def sendDataToCar(IPaddress,idCar):
    """
    This function send ssh command to the car to : stop a previous GUI program, removing old files on Receive/ folder,
    upload new files to this folder and than start the GUI program.
    It call the readingJSON() function to know which file to upload.
    To do so, the sshpass module is used :
    sudo apt-get install sshpass
    Also, the os library is used to pass system commands.
    :param IPaddress:
    :return:
    """
    file = readingJSON(idCar)
    clean = "sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@" + IPaddress + " 'rm /home/pi/Receive/*.txt'"
    print(clean)
    os.popen(clean)
    command = "sshpass -p  'raspberry' scp -o StrictHostKeyChecking=no " + file + " pi@" + IPaddress + ":Receive"
    print(command)
    os.popen(command)
    stop = "sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@" + IPaddress + " 'sudo pkill -15 -f GUIfile.py'"
    print(stop)
    os.popen(stop)
    start = "sshpass -p 'raspberry' ssh -o StrictHostKeyChecking=no pi@" + IPaddress + " 'export DISPLAY=:0 && sh GUIstart.sh &'"
    print(start)
    os.popen(start)
    time.sleep(2)
    print("message copied in Car")


def main():
    """
    It runs with exception catcher to make sure that the if an exception is catched it will be disconnected from the
    MQTT Broker and all lights will be turned off.
    Initiate the MQTT related function.
    :return:
    """
    try:
        client.on_connect = on_connect
        client.on_message = on_message
        GPIO.output(EngineOn, GPIO.HIGH)
        # Once everything has been set up, we can (finally) connect to the broker
        # 1883 is the listener port that the MQTT broker is using
        client.connect(mqtt_broker_ip, 1883)
        client.loop_forever()
    except (KeyboardInterrupt, SystemExit):  # when you press ctrl+c
        print("\nKilling Thread...")
        GPIO.output(BLEAuthenNotOk, GPIO.LOW)
        GPIO.output(BLEAuthenOk, GPIO.LOW)
        GPIO.output(EngineOn, GPIO.LOW)
        client.disconnect()
    print("Done.\nExiting.")


if __name__ == '__main__':
    # creation of a log file
    logging.basicConfig(filename='BLE_Access.log', level=logging.DEBUG)

    # setup of GPIO to managed the lights
    GPIO.setmode(GPIO.BCM)
    BLEAuthenOk = 5
    BLEAuthenNotOk = 6
    EngineOn = 13
    GPIO.setup(BLEAuthenOk, GPIO.OUT, initial=0)
    GPIO.setup(BLEAuthenNotOk, GPIO.OUT, initial=0)
    GPIO.setup(EngineOn, GPIO.OUT, initial=0)

    # MQTT
    mqtt_username = "loraroot"
    mqtt_password = "root"
    mqtt_broker_ip = "localhost"
    client = mqtt.Client()
    mqtt_BLE_topic = "/RSU/local/BLE/json"

    # Set the username and password for the MQTT client
    client.username_pw_set(mqtt_username, mqtt_password)

    # list of authorised vice that have been seen by RSU
    deviceList = []

    # call main function
    main()
