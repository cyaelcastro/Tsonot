import platform
import sys
import paho.mqtt.client as mqtt
import json
import subprocess
from pathlib import Path
import os

MQTT_BROKER = "192.168.68.199"
MQTT_ROOT_TOPIC = "tsonot/1"
MQTT_TOPICS = [(MQTT_ROOT_TOPIC+"/browser/start/+",1),(MQTT_ROOT_TOPIC+"/picture/start/+",1),
                (MQTT_ROOT_TOPIC+"/video/start/+",1),(MQTT_ROOT_TOPIC+"/end",1)]

#Base location for media files
BASE_LOCATION = "./media/"

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


def load_commands(os):
    with open("commands.json") as json_file:
        commands = json.load(json_file)
        return commands.get(os)


def generate_command(mqtt_topic, command_json):
    mqtt_topic_levels = mqtt_topic.split("/")

    if check_file_exist(mqtt_topic_levels[4]):
        command_list = command_json.get(mqtt_topic_levels[2])
        command_list.append(mqtt_topic_levels[4])
        command_list[-1] = Path(BASE_LOCATION+command_list[-1]).absolute()
        run_command(command_list)


def check_file_exist(file_name):
    return Path(BASE_LOCATION+file_name).exists()


def run_command(command_list):
    print(command_list)
    
    command_subprocess = subprocess.run(command_list, shell=True)
    

def create_mqtt_conection(commands):
    client = mqtt.Client(client_id="Tsonot", userdata=commands)
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
    
    if message.topic == MQTT_TOPICS[3][0]:
        pass
    else:
        generate_command(message.topic, userdata)
    
    

def on_log(client, userdata, level, buf):
    print("log: ",buf)


if __name__  == "__main__":
    #Check Python version and raise an error if < 3.X
    check_version()
    #Check OS to know how to handle system calls
    os = check_os()

    commands = load_commands(os)

    mqtt_client = create_mqtt_conection(commands)
    mqtt_client.loop_forever()
    
    
    
    


    