import requests
from bs4 import BeautifulSoup
import paho.mqtt.client as mqtt
import time


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
    print("On connect")


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


def sendMQTTData(result):
    """
    This function publish a JSON format file on the MQTT Broker under the topic "/RSU/remote/Traffic/json".
    It precise the deviceID and the data scrapped in Twitter.
    The QoS is 1, it is what OneM2M standard recommend.
    :param result:
    :return:
    """
    payload = ("""
    {
        "deviceID" : "Traffic",
        "Data" : %s
    }
    """ % (str(result)))

    client.publish("/RSU/remote/Traffic/json", payload, 1)


def scrapping():
    """
    This function use the requests and BeautifulSoup python libraries. This code is specific to the twitter
    webpage scrapped. To scrap information from another website this code needs to be modify.
    The text received is then clean to respect a JSON format that can be sent into the OneM2M translator.
    The information retrieved are french so the this script change them into accentfree letters.
    This sendMQTTData() function is then called to publish this information in the MQTT Broker.
    Upload the content of Traffic_information.txt
    :return:
    """
    # data = requests.get("https://twitter.com/acl_info_fr?lang=en")
    # soup = BeautifulSoup(data.text, "lxml")
    # result = []
    # time = []
    # info = []
    # trafficInfo = {}
    # for div in soup.findAll("div", {"class": "js-tweet-text-container"}):
    #     trafficInfo[div.find('p').attrs['class'][0]] = div.text.strip()
    #     trafficInfotemp = str(trafficInfo).strip('{ \'TweetTextSize\' : u\'')
    #     trafficInfotemp = trafficInfotemp.strip('}')
    #     info += [trafficInfotemp]
    #
    # spans = soup.find_all('span', attrs={'class': '_timestamp'})
    # for span in spans:
    #     time += [span.string]
    #
    # for i in range(len(time)):
    #     result += ["{\"time\" : \"" + time[i] + "\", \"Incident\" : \"" + info[i] + "\"}"]
    #
    # result_cleaned = str(result).replace('u\"', '\n')
    # result_cleaned = str(result_cleaned).replace('u\'', '\n')
    # result_cleaned = str(result_cleaned).replace('\\\'}\'', '}')
    # result_cleaned = str(result_cleaned).replace('\\\'\"}\'', '\"}')
    # result_cleaned = str(result_cleaned).replace(',\"}', '\"}')
    # result_cleaned = str(result_cleaned).replace('\"\"', '\"')
    # result_cleaned = str(result_cleaned).replace('}\'', '}')
    # result_cleaned = str(result_cleaned).replace('\\\'', ' ')
    # # change les lettres avec accent en lettres sans
    # result_cleaned = str(result_cleaned).replace('\\\\xe9', 'e')
    # result_cleaned = str(result_cleaned).replace('\\\\xe0', 'a')
    # result_cleaned = str(result_cleaned).replace('\\\\xe8', 'e')
    # result_cleaned = str(result_cleaned).replace('\\\\xf4', 'o')
    data = requests.get("https://www.acl.lu/Mobility/Trafic-Luxembourg/Info-Trafic-en")
    soup = BeautifulSoup(data.text, "lxml")
    result = []
    kind = []
    time = []
    location = []
    info = []

    pars = soup.find_all('p', attrs={'class': "font-12"})
    for par in pars:
        time += [par.string]

    divs = soup.find_all('div', attrs={'class': ["btn bck blue", "btn bck red"]})
    for div in divs:
        kind += [div.string]

    for div1 in soup.findAll("div", {"class": "box bck lightestgrey"}):
        heads = div1.find_all('h3')
        for head in heads:
            location += [head.string]

    test = soup.find_all("div", attrs={'class': "col-md-12"})
    for te in test:
        info += [te.string]

    info = filter(None, info)

    info.pop(0)

    readable_file = ""

    for i in range(len(time)):
        result += ["{ \"type\" : \"" + kind[i] + "\", \"location\" : \"" + location[i] +
                   "\", \"time\" : \"" + time[i] + "\", \"description\" : \"" + info[i] +
                   "\"}"]

        readable_file += str(kind[i]) + "\n\n" + str(time[i]) + "\n" + location[i].encode('utf-8') + "\n\n" + info[i].encode('utf-8') + "\n"

    # print(result)
    result_cleaned = str(result).replace("u\'", "")
    result_cleaned = str(result_cleaned).replace("\\r\\n    ", "")
    result_cleaned = str(result_cleaned).replace("\\xe8", "e")
    result_cleaned = str(result_cleaned).replace("\\xe9", "e")
    result_cleaned = str(result_cleaned).replace("\\", " ")
    result_cleaned = str(result_cleaned).replace("\'", "")

    sendMQTTData(result_cleaned)


    print(readable_file)
    f = open("Receive/Traffic_information.txt", "a+")
    f.write(readable_file + "\n")
    f.close()


def main():
    """
    main function initiate the MQTT related function and connect to the broker.
    It runs a while True loop with exception catcher to make sure that the
    loop will not stopped. Then, every 120 seconds, it scrap information on twitter and send it to the MQTT Broker.
    :return:
    """
    try:
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(mqtt_broker_ip, 1883)
        client.loop_start()
        while True:
            scrapping()
            time.sleep(120)
    except (KeyboardInterrupt, SystemExit):
        print("\nKilling Thread...")
        client.disconnect()
    print("Done.\nExiting.")


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
