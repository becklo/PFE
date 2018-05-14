import paho.mqtt.client as mqtt
import json #parse messages


# def sendOneM2MMqttDataRPI(msg):
#     global rqi
#     if msg.topic == mqtt_rsu_topic:
#         parsed_json = json.loads(str(msg.payload))
#         timestamp = parsed_json['RoadsideUnit_Status']['Current_Readings']['DHT_Sensor_3_(Rpi3)']['Timestamp']
#         sen_temp = parsed_json['RoadsideUnit_Status']['Current_Readings']['DHT_Sensor_3_(Rpi3)']['Temperature']
#         sen_hum = parsed_json['RoadsideUnit_Status']['Current_Readings']['DHT_Sensor_3_(Rpi3)']['Humidity']
#         gpsLatitude = parsed_json['RoadsideUnit_Status']['Current_Readings']['GPS_Location']['Latitude']
#         gpsLongitude = parsed_json['RoadsideUnit_Status']['Current_Readings']['GPS_Location']['Longitude']
#         rpiData = ("""
#             {
#                 "m2m:rqp": {
#                     "m2m:fr": "admin:admin",
#                     "m2m:to": "/mn-cse/mn-name/RSU/DATA",
#                     "m2m:op": 1,
#                     "m2m:rqi": "%s",
#                     "m2m:pc": {
#                         "m2m:cin": {
#                             "cnf": "RSU",
#                             "con":  "{
#                                     \'appId\' : \'RSU\',
#                                     \'completeData\' : [{
#                                         \'timestamp\' : \'%s\'
#                                         },
#                                         {\'category\' : \'temperature\',
#                                         \'data\' : \'%s\',
#                                         \'unit\' : \'Celsius\'
#                                         },
#                                         {\'category\' : \'humidity\',
#                                         \'data\' : \'%s\',
#                                         \'unit\' : \'Percent\'
#                                         },
#                                         {\'position\' :[{
#                                             \'category\' : \'latitude\',
#                                             \'data\' : \'%s\',
#                                             \'unit\' : \'Metre\'
#                                             },
#                                             {\'category\' : \'Longitude\',
#                                             \'data\' : \'%s\',
#                                             \'unit\' : \'Metre\'
#                                             }]
#                                         }]
#                                     }"
#                         }
#                     },
#                     "m2m:ty": 4
#                 }
#             }
#             """%(rqi,timestamp,sen_temp,sen_hum,gpsLatitude,gpsLongitude))
#         client.publish("/oneM2M/req/RSU/mn-cse/json",rpiData,1)
#         rqi += 1
#         print("Send:", rpiData)
#         rqi = rqi%max_id


def sendOneM2MMqttDataSensor(msg):
    """
    This function translate all the sensor related messages into OneM2M convenient messages and send it under the 
    right topic on the MQTT Broker. It includes the sensors and the weather information received from the weather 3rd
    party service.
    The QoS is 1, it is what OneM2M standard recommend.
    :param msg: 
    :return: 
    """
    global rqi
    parsed_json = json.loads(str(msg.payload))
    dev_id=parsed_json['deviceID']
    temperature=str(parsed_json['Data']["Temperature"]["data"])
    humidity = str(parsed_json['Data']["Humidity"]["data"])
    timestamp = str(parsed_json['Data']["Timestamp"])
    payload = ("""
        {
            "m2m:rqp": {
                "m2m:fr": "admin:admin",
                "m2m:to": "/mn-cse/mn-name/%s/DATA",
                "m2m:op": 1,
                "m2m:rqi": "%s",
                "m2m:pc": {
                    "m2m:cin": {
                        "cnf": "%s",
                        "con":  "{
                                \'appId\' : \'%s\',
                                \'completeData\' : [{
                                    \'timestamp\' : \'%s\'
                                    },
                                    {\'category\' : \'temperature\',
                                    \'data\' : \'%s\',
                                    \'unit\' : \'Celsius\'
                                    },
                                    {\'category\' : \'humidity\',
                                    \'data\' : \'%s\',
                                    \'unit\' : \'Percent\'
                                    }]
                                }"
                    }
                },
                "m2m:ty": 4
            }
        }
        """%(dev_id, rqi, dev_id, dev_id, timestamp, temperature, humidity))
    client.publish("/oneM2M/req/{}/mn-cse/json".format(dev_id), payload, 1)
    rqi += 1
    print("Send:", payload)
    rqi = rqi%max_id


def sendOneM2MMqttGPSData(msg):
    """
     This function translate all the GPS related messages into OneM2M convenient messages and send it under the 
    right topic on the MQTT Broker. 
    The QoS is 1, it is what OneM2M standard recommend.
    :param msg: 
    :return: 
    """
    global rqi
    parsed_json = json.loads(str(msg.payload))
    dev_id = parsed_json['deviceID']
    latitude = str(parsed_json['Data']["gpsLatitude"])
    longitude = str(parsed_json['Data']["gpsLongitude"])
    payload = ("""
           {
               "m2m:rqp": {
                   "m2m:fr": "admin:admin",
                   "m2m:to": "/mn-cse/mn-name/%s/DATA",
                   "m2m:op": 1,
                   "m2m:rqi": "%s",
                   "m2m:pc": {
                       "m2m:cin": {
                           "cnf": "%s",
                           "con":  "{
                                   \'appId\' : \'%s\',
                                   \'completeData\' : [{
                                       {\'category\' : \'latitude\',
                                       \'data\' : \'%s\',
                                       \'unit\' : \'Meter\'
                                       },
                                       {\'category\' : \'longitude\',
                                       \'data\' : \'%s\',
                                       \'unit\' : \'Meter\'
                                       }]
                                   }"
                       }
                   },
                   "m2m:ty": 4
               }
           }
           """ % (dev_id, rqi, dev_id, dev_id, latitude, longitude))
    client.publish("/oneM2M/req/{}/mn-cse/json".format(dev_id), payload, 1)
    rqi += 1
    print("Send:", payload)
    rqi = rqi % max_id


def sendOneM2MMqttTrafficData(msg):
    """
     This function translate all the traffic related messages into OneM2M convenient messages and send it under the 
    right topic on the MQTT Broker. 
    The QoS is 1, it is what OneM2M standard recommend.
    :param msg: 
    :return: 
    """
    global rqi
    parsed_json = json.loads(str(msg.payload))
    dev_id = parsed_json['deviceID']
    trafficInfo = str(parsed_json['Data'])
    payload = ("""
               {
                   "m2m:rqp": {
                       "m2m:fr": "admin:admin",
                       "m2m:to": "/mn-cse/mn-name/%s/DATA",
                       "m2m:op": 1,
                       "m2m:rqi": "%s",
                       "m2m:pc": {
                           "m2m:cin": {
                               "cnf": "%s",
                               "con":  "{
                                       \'appId\' : \'%s\',
                                       \'completeData\' : {
                                           {\'category\' : \'TrafficInfo\',
                                           \'data\' : \'%s\'
                                           }
                                       }"
                           }
                       },
                       "m2m:ty": 4
                   }
               }
               """ % (dev_id, rqi, dev_id, dev_id, trafficInfo))
    client.publish("/oneM2M/req/{}/mn-cse/json".format(dev_id), payload, 1)
    rqi += 1
    print("Send:", payload)
    rqi = rqi % max_id


def translation(msg, topic):
    """
    This function sort the topics to call the adequate function for the translation.
    :param msg: 
    :param topic: 
    :return: 
    """
    if topic == "Sensor1" or topic == "Sensor2" or topic == "Sensor3" or topic == "WeatherMap":
        sendOneM2MMqttDataSensor(msg)
    if topic == "GPSMouse":
        sendOneM2MMqttGPSData(msg)
    if topic == "Traffic":
        sendOneM2MMqttTrafficData(msg)


def on_connect(client, userdata, flags, rc):
    """
    rc is the error code returned when connecting to the broker
    Once the client has connected to the broker, subscribe to the topic you are interested in.
    Here it is all the topics from the RSU.
    :param client: 
    :param userdata: 
    :param flags: 
    :param rc: 
    :return: 
    """
    client.subscribe(mqtt_rsu_topic)


def on_message(client, userdata, msg):
    """
    MQTT on message callback method.
    This function is called everytime the topic is published to.
    If you want to check each message, and do something depending on
    the content, the code to do this should be run in this function.
    Here the topic is check and if it hasn't been seen before the creation of containers and application is done
    so the automation of generated responses can be done. Then the translation() method is call to sort the messages.
    :param client: 
    :param userdata: 
    :param msg: 
    :return: 
    """
    print("Message received, sendind translation")
    print(msg.topic)
    global topic_list
    topic = str(msg.topic).split("/", 4)[3]
    print(topic)
    if topic not in topic_list:
        CSEPublish(topic)
        AEPublish(topic)
        ContCrea(topic)
        topic_list += {topic}
    print(topic_list)
    translation(msg, topic)


def CSEPublish(topic):
    """
    This function publish a CSE request on the MQTT broker. It is mandatory to publish this request for each different
    topic.
    :param topic: 
    :return: 
    """
    payload = ("""
    {
       "m2m:rqp": {
          "m2m:fr": "%s",
          "m2m:to": "/mn-cse",
          "m2m:op": 2,
          "m2m:rqi": 1111111
       }
    }
    """ %topic)
    client.publish("/oneM2M/req/{}/mn-cse/json".format(topic), payload, 1)


def AEPublish(topic):
    """
    This function publish a AE request on the MQTT broker. It is mandatory to publish this request for each different
    topic.
    :param topic: 
    :return: 
    """
    payload = ("""
    {
        "m2m:rqp": {
            "m2m:fr" : "admin:admin",
            "m2m:to" : "/mn-cse/mn-name",
            "m2m:op" : 1,
            "m2m:rqi": 2222222,
            "m2m:pc": {
                "m2m:ae": {
                "api": "123",
                "rr": "true",
                "rn": "%s"
                }
            },
            "m2m:ty": 2
            }
    }
    """ % topic)
    client.publish("/oneM2M/req/{}/mn-cse/json".format(topic), payload, 1)


def ContCrea(topic):
    """
    This function publish a Container Creation request on the MQTT broker. It is mandatory to publish this request for each different
    topic.
    :param topic: 
    :return: 
    """
    payload = ("""
    {
        "m2m:rqp" : {
            "m2m:fr" : "admin:admin",
            "m2m:to" : "/mn-cse/mn-name/%s",
            "m2m:op" : 1,
            "m2m:rqi": 123456,
            "m2m:pc": {
                "m2m:cnt" : {
                    "rn": "DATA"
                }
            },
            "m2m:ty": 3
        }
    }
    """ % topic)
    client.publish("/oneM2M/req/{}/mn-cse/json".format(topic), payload, 1)


def main():
    """
    It runs a while True loop with exception catcher to make sure that the
    loop will not stopped. Initiate the MQTT related function.
    Has exception to be able to disconnect from the MQTT Broker.
    :return: 
    """
    try:
        client.on_connect = on_connect
        client.on_message = on_message
        client.subscribe(mqtt_topic_oneM2M)
        client.connect(mqtt_broker_ip, 1883)
        client.loop_forever()
    except (KeyboardInterrupt, SystemExit):
        print("\nKilling Thread...")
        client.disconnect()
    print("Done.\nExiting.")


if __name__ == '__main__':
    # MQTT
    mqtt_username = "loraroot"
    mqtt_password = "root"
    mqtt_rsu_topic = "/RSU/+/+/json"
    mqtt_topic_oneM2M = "/oneM2M/resp/+/mn-cse/json"
    mqtt_broker_ip = "localhost"

    client = mqtt.Client()
    # Set the username and password for the MQTT client
    client.username_pw_set(mqtt_username, mqtt_password)

    topic_list = []
    max_id = 1000
    rqi = 0

    # call main function
    main()


