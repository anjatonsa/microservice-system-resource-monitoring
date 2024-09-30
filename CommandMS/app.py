from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt
import json , requests, os

app = Flask(__name__)

broker_address = "mosquitto"
broker_port = 1883
sub_topic = "notification/+"

APIGATEWAY_URL = os.getenv('APIGATEWAY_URL')

def pass_notf(msg):
    requests.post(f"{APIGATEWAY_URL}/notify",json=msg)
    return


def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code "+str(rc))
    client.subscribe(sub_topic, qos=0)
    print("Subcribed to topic " + sub_topic)

def on_message(client, userdata, msg):
    message_data = json.loads(msg.payload.decode())
    print(f"Received message from topic {msg.topic}, {message_data}")
    pass_notf(message_data)
    print("Passed the notification to APIGatewayMS.")


@app.route('/')
def index():
    return 'Command  microservice'

if __name__ == '__main__':

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker_address, broker_port, 0)
    client.loop_start()


    app.run(host="0.0.0.0", port=5001)
