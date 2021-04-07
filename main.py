import platform
import sys
import paho.mqtt.client as mqtt
import json
import subprocess
from pathlib import Path
import os
import time

MQTT_BROKER = "192.168.68.113"
MQTT_ROOT_TOPIC = "tsonot/1"
MQTT_TOPICS = [(MQTT_ROOT_TOPIC+"/browser/start/+",1),(MQTT_ROOT_TOPIC+"/picture/start/+",1),
                (MQTT_ROOT_TOPIC+"/video/start/+",1),(MQTT_ROOT_TOPIC+"/end",1)]

#Base location for media files
BASE_LOCATION = "./media/"

#Flag to show the log in the MQTT connection
LOG_ACTIVATED = 0

command_executed = []

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
        kill_command = command_json.get("kill_pid")
        run_command(command_list, kill_command)


def check_file_exist(file_name):
    return Path(BASE_LOCATION+file_name).exists()


def run_command(command_list, kill_command):
    
    #Declare commmand executed as global to record the last process executed
    global command_executed

    #In case of a previous process in execution
    if command_executed:
        execute_kill_command(command_executed, kill_command)

    #Wait for killing the previous process
    time.sleep(2)

    print("Running process: ", command_list[1])
    command_subprocess = subprocess.run(command_list, shell=True, capture_output=True, text=True)

    #If the command_subprocess generate an error will be printed    
    if command_subprocess.stderr:
        print("stderror:", command_subprocess.stderr)
    
    #Record the executed command in command_executed var
    command_executed = command_list

    #Return the executed command to previous state before adding the file
    command_executed.pop()


def execute_kill_command(command_list, kill_command):
    
    #Append name of the process to be killed to the kill command list
    kill_command.append(command_list[1])
    
    #Add process extension
    kill_command[-1]= kill_command[-1]+".exe"
    
    #Indicate what process is going to be killed
    print("Killing process: ",kill_command[-1])

    #Create the subprocess to execute the kill command, 
    kill_subprocess = subprocess.run(kill_command, shell=True, text=True)
    
    #Show the return code of the subprocess, if not zero
    if kill_subprocess.returncode != 0:
        print("Killing process status: ",kill_subprocess.returncode)
    
    #Restore the command list to initial state, without process executed
    kill_command.pop()


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
    
    
    
    


    