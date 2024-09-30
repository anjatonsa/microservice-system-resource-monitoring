from flask import Flask
import paho.mqtt.client as mqtt
import json,os,requests
import numpy as np

app = Flask(__name__)

broker_address = "mosquitto"
broker_port = 1883
sub_topic = "sensor/readings"
pub_topic_cpu = "notification/cpu_load"
pub_topic_power = "notification/power"

MLMODEL_URL = os.getenv('MLMODEL_URL')

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code "+str(rc))
    client.subscribe(sub_topic, qos=0)
    print("Subcribed to topic " + sub_topic)

def on_publish(client, userdata, result):
    print("Data published from AnalyticsMS.")

def on_message(client, userdata, msg):
    message_data = json.loads(msg.payload.decode())
    print(f"Received message from topic {msg.topic}, {message_data}")

    #poziv mlmodel servisa
    cpu_load_response = requests.post(f"{MLMODEL_URL}/predict/cpuload",json=message_data)
    power_consp_response = requests.post(f"{MLMODEL_URL}/predict/power",json=message_data)
    
    if cpu_load_response.status_code == 200 and power_consp_response.status_code == 200:
        cpu_load_prediction = cpu_load_response.json()
        power_consp_prediction = power_consp_response.json()
        handle_prediction(cpu_load_prediction, power_consp_prediction)
    else:
        print("Failed to get predictions from the ML model service")


def handle_prediction(cpu_load_prediction, power_prediction):
    print("Analytics received predictions from MLModelMS.")
    message = {}
    message['time'] = cpu_load_prediction['time_value']
    message['cpu_load'] = cpu_load_prediction['cpu_load_prediction']

    if cpu_load_prediction['cpu_load_prediction'] > 80:  # CPU load greater than 80%
        message['cpu_load_message'] = "High CPU load!"
    else:
        message['cpu_load_message'] = "Normal CPU load."
    
    json_message = json.dumps(message)
    client.publish(pub_topic_cpu, json_message)
    print("Published CPU_Load value = ", message['cpu_load'])
    
    message = {}
    message['time'] = power_prediction['time_value']
    message['power'] = power_prediction['power_prediction']
    
    if power_prediction['power_prediction'] > 170:  # Power greater than 170 Watts
        message['power_message'] = "High power consumption!"
    else:
        message['power_message'] = "Normal power consumption."
        
    json_message = json.dumps(message)
    client.publish(pub_topic_power, json_message)
    print("Published predicted Power value = ", message['power'])

@app.route('/')
def index():
    return 'Analytics  microservice'


if __name__ == '__main__':

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message

    client.connect(broker_address, broker_port, 0)
    client.loop_start()

    app.run()
