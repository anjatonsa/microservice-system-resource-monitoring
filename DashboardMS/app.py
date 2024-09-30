import os,json
from flask import Flask, jsonify
import paho.mqtt.client as mqtt
from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv


app = Flask(__name__)

broker_address = "mosquitto"
broker_port = 1883
sub_topic = "sensor/readings"

load_dotenv()
url = os.getenv('URL', None)
org = os.getenv('ORG', None)
token = os.getenv('TOKEN',None)
bucket = os.getenv('BUCKET', None)

@app.route('/')
def index():
    return 'Dashboard microservice'

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe(sub_topic, qos=0)
    print("Subcribed to topic " + sub_topic)

def on_message(client, userdata, msg):
    message_data = json.loads(msg.payload.decode())
    print(f"Received message from topic {msg.topic}, {message_data}")
    process_messages(message_data)

def process_messages(msg):
    try:          
            point = Point("sensor_readings").time(datetime.strptime(msg['Time'], '%Y-%m-%d %H:%M:%S').isoformat())
            for key, value in msg.items():
                if key == 'Time':
                    continue
                else:
                    point = point.field(key, value)
            write_api.write(bucket, org, point)
            print("Data successfully written to InfluxDB")
    except Exception as e:
            print(f"Error storing data in InfluxDB: {e}")

@app.route('/get_snapshot', methods=['GET'])
def get_snapshot():  
    print("/get_snapshot route is called.")
    try:
        snapshot_url = os.getenv('SNAPSHOT-URL', None)
        return jsonify({"snapshot_url": snapshot_url}), 200
    except Exception as e:
        return jsonify({"error": e}), 500


if __name__ == '__main__':

    client = InfluxDBClient(url=url, token=token, org=org)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker_address, broker_port, 60)
    client.loop_start()
    app.run(host="0.0.0.0", port=5002)
