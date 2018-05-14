import sys
import os
import time


def optionDisplay():
    """
    This function just display the available options of this script.
    :return:
    """
    print("Options :")
    print("[-All] : to start all the Microservices listed below")
    print("[-B] : to start the Bluetooth Low Energy MicroService")
    print("[-C] : to start the Cloud MicroService")
    print("[-G] : to start the GPS MicroService")
    print("[-h] : to display the usage")
    print("[-S] : to start the Sensor Data gathering MicroService")
    print("[-t] : to start the traffic MicroService")
    print("[-T] : to start the Translator MicroService this takes some times")
    print("[-W] : to start the Weather MicroService")


def startBLE(serviceList):
    """
    This function start the MS_BLE.py program using a system request
    :return:
    """
    print("trying to start BLE")
    os.system('sudo python MS_BLE.py &')
    serviceList += {"MS_BLE.py"}
    print("BLE started")


def startCloud(serviceList):
    """
    This function start the MS_Cloud.py program using a system request
    :return:
    """
    print("trying to start Cloud")
    os.system('python MS_Cloud.py &')
    serviceList += {"MS_Cloud.py"}
    print("Cloud started")


def startGPS(serviceList):
    """
    This function start the MS_GPS.py program using a system request
    :return:
    """
    print("trying to start GPS")
    os.system('sudo python MS_GPS.py &')
    serviceList += {"MS_GPS.py"}
    print("GPS started")


def startSensor(serviceList):
    """
    This function start the MS_SensorData.py program using a system request
    :return:
    """
    print("trying to start Sensor")
    os.system('python MS_SensorData.py &')
    serviceList += {"MS_SensorData.py"}
    print("SensorData started")


def startTraffic(serviceList):
    """
    This function start the MS_Traffic.py program using a system request
    :return:
    """
    print("trying to start Traffic")
    os.system('python MS_Traffic.py &')
    serviceList += {"MS_Traffic.py"}
    print("Traffic started")


def startTranslator(serviceList):
    """
    This function calls a bash script using a system request. This script is meant to start the Eclipse OM2M project
    and the MQTT plugin. It takes some time so to be sure that is it fully launch before starting the MS_Translator.py
    python program using a system request it wait 10 seconds.
    :return:
    """
    print("Starting OM2M project")
    os.system("sh ./../Controller.sh")
    time.sleep(30)
    print("OM2M project started")
    print("trying to start Translator")
    os.system('python MS_Translator.py &')
    serviceList += {"MS_Translator.py"}
    print("Translator started")


def startWeather(serviceList):
    """
    This function start the MS_Weather.py program using a system request
    :return:
    """
    print("trying to start Weather")
    os.system('python MS_Weather.py &')
    serviceList += {"MS_Weather.py"}
    print("Weather started")


def killService(name, serviceList):
    """
    This function kill with option -15 so it can terminate its action before beeing killed. It uses the pkill -f command
    to be able to kill a service with its name only. The list of services running is then updated
    :param name:
    :param serviceList:
    :return:
    """
    command = "pkill -15 -f " + name
    print(command)
    os.system(command)
    serviceList.remove(name)
    print(serviceList)


def sorting(arguments,serviceList):
    """
    This function is acting like a switch depending on the arguments. For now it doesn't check if some service needs
    other services to be running. If no valid arguments are given it display the valid options.
    :param arguments:
    :return:
    """
    length = len(arguments)
    if length == 1:
        print("Argument from the list below are needed : ")
        optionDisplay()
    for i in range(1, length):
        if arguments[i] == '-h':
            optionDisplay()
            break
        elif arguments[i] == '-All':
            startTranslator(serviceList)
            # let some time to start everything for the translation
            time.sleep(20)
            startBLE(serviceList)
            startCloud(serviceList)
            startGPS(serviceList)
            startSensor(serviceList)
            startTraffic(serviceList)
            startWeather(serviceList)

            break
        elif arguments[i] == '-B':
            startBLE(serviceList)
        elif arguments[i] == '-C':
            startCloud(serviceList)
        elif arguments[i] == '-G':
            startGPS(serviceList)
        elif arguments[i] == '-S':
            startSensor(serviceList)
        elif arguments[i] == '-t':
            startTraffic(serviceList)
        elif arguments[i] == '-T':
            startTranslator(serviceList)
        elif arguments[i] == '-W':
            startWeather(serviceList)
        else:
            print("The argument must be from : ")
            optionDisplay()
            break


def main():
    """
    main function that calls the sorting method transmitting the arguments given.
    :return:
    """
    try:
        serviceList = []
        sorting(sys.argv, serviceList)
        while True:
            # noting
            pass
    except (KeyboardInterrupt, SystemExit):  # when you press ctrl+c
        print("\nKilling Thread...")
        # kill OM2M project
        os.system("sudo killall -9 java")
        os.system("echo")
        # kill all microservices
        os.system("sudo killall -15 python")
        print("Done.\nExiting.")


if __name__ == '__main__':
    # call main function
    main()