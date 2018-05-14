
# Import the necessary libraries

from __future__ import print_function
import paho.mqtt.client as mqtt
import json
import time
import pyowm


def on_connect(client, userdata, flags, rc):
    """
    rc is the error code returned when connecting to the broker
    Once the client has connected to the broker, subscribe to the topic you are interested in.
    Here it subscribe to the GPS topic to get location information.
    :param client:
    :param userdata:
    :param flags:
    :param rc:
    :return:
    """
    client.subscribe(mqtt_gps_topic)


def on_message(client, userdata, msg):
    """
    MQTT on message callback method.
    This function is called everytime the topic is published to.
    If you want to check each message, and do something depending on
    the content, the code to do this should be run in this function.
    Here each time it receives a location information the getWeatherInfo() function is called.
    :param client:
    :param userdata:
    :param msg:
    :return:
    """
    getWeatherInfo(msg)


def getWeatherInfo(msg):
    """
    This function retrieve the GPS information from the payload of the received message and then do a request to the 
    Open WeatherMap website with the pyowm python library. Then only the temperature and humidity information are 
    saved. 
    Once the information is saved the sendMQTTData() function is called.
    :param msg: 
    :return: 
    """
    parsed_json = json.loads(str(msg.payload))
    latitude = parsed_json["Data"]["gpsLatitude"]
    longitude = parsed_json["Data"]["gpsLongitude"]
    observation_list = owm.weather_around_coords(float(latitude), float(longitude))
    w = observation_list[0].get_weather()
    humidity = w.get_humidity()
    temperature = w.get_temperature('celsius')
    sendMQTTData(temperature, humidity)


def sendMQTTData(temperature, humidity):
    """
    This function publish a JSON format file on the MQTT Broker under the topic "/RSU/remote/WeatherMap/json".
    It precise the deviceID and all the data gathered with the pyowm request. A timestamp is added.
    The QoS is 1, it is what OneM2M standard recommend.
    Update the content of Weather.txt.
    :param temperature: 
    :param humidity: 
    :return: 
    """
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()))
    payload = ("""
    {
        "deviceID" : "WeatherMap",
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
    """%(temperature, humidity, timestamp))
    client.publish("/RSU/remote/WeatherMap/json", payload, 1)

    f = open("Receive/Weather.txt", "a+")
    f.write(payload + "\n")
    f.close()


def main():
    """
    main function initiate the MQTT related function and connect to the broker.
    It runs a while True loop with exception catcher to make sure that the
    loop will not stopped.
    :return:
    """
    try:
        client.on_connect = on_connect
        client.on_message = on_message
        # Once everything has been set up, we can (finally) connect to the broker
        # 1883 is the listener port that the MQTT broker is using
        client.connect(mqtt_broker_ip, 1883)
        client.loop_forever()
    except (KeyboardInterrupt, SystemExit):
        print("\nKilling Thread...")
        client.disconnect()
    print("Done.\nExiting.")


if __name__ == '__main__':
    # My valid API key
    owm = pyowm.OWM('13ca5ee5f57c88c6f0d23be056c59506')

    # MQTT
    mqtt_username = "loraroot"
    mqtt_password = "root"
    mqtt_broker_ip = "localhost"
    mqtt_gps_topic = "/RSU/local/GPSMouse/json"
    client = mqtt.Client()

    # Set the username and password for the MQTT client
    client.username_pw_set(mqtt_username, mqtt_password)
    # call main function
    main()
