import argparse
import paho.mqtt.client as mqtt
import time
import signal
import subprocess

loop_flag = 1
user_exit = False
relay_path = "/your/path/to/raspiRelayController/wiringPiController"

mqttUserName = "your-broker-username-here"
mqttPassword = "your-broker-password-here"

def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default

def perform_heating(param1):
    print("raspiRelayControllerListener: perform_heating.")

def perform_air_cond(param1):    
    print("raspiRelayControllerListener: perform_air_cond.")
    if param1 == 0:
        cmd = [relay_path + '/runRemoteControlAir1.sh']
    elif param1 == 1:
        cmd = [relay_path + '/runRemoteControlAir0.sh']
    else:
        return
    print(cmd)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    process.wait()

def on_message(client, userdata, message):
    print("raspiRelayControllerListener: message received ", str(message.payload.decode("utf-8")))
    print("raspiRelayControllerListener: message topic=", message.topic)
    print("raspiRelayControllerListener: message qos=", message.qos)
    print("raspiRelayControllerListener: message retain flag=", message.retain)

    the_int_string = message.payload.decode("utf-8")
    the_int = safe_cast(message.payload, int) 
    if the_int is None:
        return

    the_int_test = the_int == 0 or the_int == 1
    if not the_int_test:
        return
    if message.retain == 1:
        return

    if message.topic == "home/garage/setHeating":
        perform_heating(the_int)
        the_topic = "home/garage/heating"
        client.publish(the_topic, the_int, 0, True)
    elif message.topic == "home/garage/setAirCond":
        perform_air_cond(the_int)
        the_topic = "home/garage/airCond"
        client.publish(the_topic, the_int, 0, True)
    else:
        print("raspiRelayControllerListener: received unknown topic.")

def on_handlesignal(param1, param2):
    print("raspiRelayControllerListener: on_handlesignal.")
    global user_exit
    user_exit = True
    global loop_flag
    loop_flag = 0    

def on_connect(client, userdata, flags, rc):
    print("raspiRelayControllerListener: on_connect.")
    global fail_count
    
def on_disconnect(client, userdata, rc=0):
    print("raspiRelayControllerListener: on_disconnect.")
    global loop_flag
    loop_flag = 0
    
    if user_exit == True:
      return

def performConnect():
    client = mqtt.Client()
    client.on_disconnect = on_disconnect
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(mqttUserName, mqttPassword)
    
    theIntPort = safe_cast(brokerPort, int)
    if theIntPort is None:
        return
    
    print("raspiRelayControllerListener: connecting...")
    client.connect(brokerUrl, theIntPort)
    
    thetopic = "home/garage/setAirCond"
    client.subscribe(thetopic)    
    
    the_topic2 = "home/garage/setHeating"
    client.subscribe(the_topic2)
    
    return client

def main(brokerUrl, brokerPort):
    client = performConnect()   
    client.loop_start()  # start the loop

    signal.signal(signal.SIGINT, on_handlesignal)
    signal.signal(signal.SIGTERM, on_handlesignal)    

    while loop_flag == 1:
        time.sleep(1)

    client.disconnect()
    client.loop_stop()

parser = argparse.ArgumentParser(description='main')
parser.add_argument('--brokerUrl', required=True, type=str)
parser.add_argument('--brokerPort', required=True, type=str)
args = parser.parse_args()
brokerUrl = args.brokerUrl
brokerPort = args.brokerPort

main(brokerUrl, brokerPort)
