
# Import the necessary libraries

from __future__ import print_function
import paho.mqtt.client as mqtt
import gps
import json
import time
import os


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


def sendMQTTData(gpsLatitude, gpsLongitude, gpsSource):
    """
    This function publish a JSON format file on the MQTT Broker under the topic "/RSU/local/GPSMouse/json".
    It precise the deviceID and all the data gathered with the GPS Mouse (gpsLatitude,gpsLongitude,gpsSource).
    The QoS is 1, it is what OneM2M standard recommend.
    Update the GPS.txt file.
    :param gpsLatitude:
    :param gpsLongitude:
    :param gpsSource:
    :return:
    """
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()))
    payload = ("""
    {
        "deviceID" : "GPSMouse",
        "Data" :{
                    "gpsLatitude" : "%s",
                    "gpsLongitude" : "%s",
                    "unit" : "m",
                    "gpsSource" : "%s",
                    "timestamp" : "%s"
                }
    }
    """ % (gpsLatitude, gpsLongitude, gpsSource, timestamp))
    client.publish("/RSU/local/GPSMouse/json", payload, 1)

    f = open("Receive/GPS.txt", "a+")
    f.write(payload + "\n")
    f.close()


def main():
    """
    main function make sure the GPS Mouse is connected, set it o the right port, enable the stream, initiate the MQTT
    related function and connect to the broker. It runs a while True loop with exception catcher to make sure that the
    loop will not stopped. Then, every 10 seconds, it reads the data from the GPS Mouse, either it receive some and save
    they or it read the information from a JSON file.
    :return:
    """
    try:
        os.system('sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock')
        gpsd = gps.gps("localhost", "2947")
        gpsd.stream(gps.WATCH_ENABLE) # starting the stream of info
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(mqtt_broker_ip, 1883)
        client.loop_start()
        while True:
          gpsd.next() # this will continue to loop and grab EACH set of gpsd info to clear the buffer
          if gpsd.fix.mode > 1:
              if gpsd.fix.mode == 2:
                  gpsSource = "2D GPS Mouse"
              else:
                  gpsSource = "3D GPS Mouse"
              gpsLatitude = gpsd.fix.latitude
              gpsLongitude = gpsd.fix.longitude
          else:
              # no GPS data
              # file with data in case of no GPS data
              parsedGPS_json = json.load(open('rsu_gps.json'))
              gpsSource = "File"
              gpsLatitude=parsedGPS_json['latitude']
              gpsLongitude=parsedGPS_json['longitude']
          sendMQTTData(gpsLatitude, gpsLongitude, gpsSource)
          time.sleep(10)

    except (KeyboardInterrupt, SystemExit): # when you press ctrl+c
        print ("\nKilling Thread...")
        client.disconnect()
    print ("Done.\nExiting.")


if __name__ == '__main__':
    # MQTT
    mqtt_username = "loraroot"
    mqtt_password = "root"
    mqtt_broker_ip = "localhost"
    client = mqtt.Client()

    # Set the username and password for the MQTT client
    client.username_pw_set(mqtt_username, mqtt_password)
    # call main function
    main()