import platform
import sys
import paho.mqtt.client as mqtt

MQTT_BROKER = "192.168.15.195"
MQTT_TOPICS = [("tsonot/1/browser/start",1),("tsonot/1/picture/start",1),("tsonot/1/video/start",1),("tsonot/1/browser/end",1),("tsonot/1/picture/end",1),("tsonot/1/video/end",1)]
#Flag to show the log in the MQTT connection
LOG_ACTIVATED = 1


def check_version():
    print("Checking Python version")
    if sys.version_info.major < 3:
        raise AttributeError("Minimum version requires is 3.x")
    print("Python version: {0}.{1} OK".format(sys.version_info.major, sys.version_info.minor))


def check_os():
    print("OS: {0}".format(platform.system()))
    return platform.system()


def create_mqtt_conection():
    client = mqtt.Client("Tsonot")
    client.on_connect=on_connect
    if LOG_ACTIVATED:
        client.on_log=on_log
    
    try:
        client.connect(MQTT_BROKER)
    except TimeoutError:
        print("Error in connection with broker")
        exit(1)
        
    client.on_message=on_message
    client.subscribe(MQTT_TOPICS)
    return client


def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True
        print("Connection OK")


def on_message(client, userdata, message):
    if message.topic == MQTT_TOPICS[0][0]:
        print("message topic=",message.topic)
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message qos=",message.qos)
    if message.topic == MQTT_TOPICS[1][0]:
        print("message topic=",message.topic)
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message qos=",message.qos)
    if message.topic == MQTT_TOPICS[2][0]:
        print("message topic=",message.topic)
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message qos=",message.qos)
    if message.topic == MQTT_TOPICS[3][0]:
        print("message topic=",message.topic)
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message qos=",message.qos)
    if message.topic == MQTT_TOPICS[4][0]:
        print("message topic=",message.topic)
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message qos=",message.qos)
    if message.topic == MQTT_TOPICS[5][0]:
        print("message topic=",message.topic)
        print("message received " ,str(message.payload.decode("utf-8")))
        print("message qos=",message.qos)


def on_log(client, userdata, level, buf):
    print("log: ",buf)


if __name__  == "__main__":
    #Check Python version and raise an error if < 3.X
    check_version()
    #Check OS to know how to handle system calls
    os = check_os()

    mqtt_client = create_mqtt_conection()
    mqtt_client.loop_forever()
    
    
    
    


    