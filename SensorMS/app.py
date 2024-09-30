from flask import Flask
import paho.mqtt.client as mqtt
import threading,time,csv,json

app = Flask(__name__)

broker_address = "mosquitto"
broker_port = 1883
pub_topic = "sensor/readings"
dataset_path="simulation_data.csv"

class SensorReading:

    def __init__(self, Series, Time, CPU_Load, Power, Network_RX, Network_TX, Inlet_Temperature,
                 CPU1_Temperature, CPU2_Temperature, Fan_speed1, Fan_speed2, Fan_speed3,
                 Fan_speed4, Ram, Ram_Used, No_Of_Running_vms, CPU_cores, CPU_cores_used):
        
        self.Series = Series
        self.Time = Time
        self.CPU_Load = CPU_Load
        self.Power = Power
        self.Network_RX = Network_RX
        self.Network_TX = Network_TX
        self.Inlet_Temperature = Inlet_Temperature
        self.CPU1_Temperature = CPU1_Temperature
        self.CPU2_Temperature = CPU2_Temperature
        self.Fan_speed1 = Fan_speed1
        self.Fan_speed2 = Fan_speed2
        self.Fan_speed3 = Fan_speed3
        self.Fan_speed4 = Fan_speed4
        self.Ram = Ram
        self.Ram_Used = Ram_Used
        self.No_Of_Running_vms = No_Of_Running_vms
        self.CPU_cores = CPU_cores
        self.CPU_cores_used = CPU_cores_used

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code "+str(rc))

def on_publish(client, userdata, result):
    print("Data published to topic ", pub_topic)

def simulate_sensor_data(client, msg):
    with open(dataset_path, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        for row in csv_reader:
            reading = SensorReading(
                Series=row[0],
                Time=row[1],
                CPU_Load=float(row[2]),
                Power=float(row[3]),
                Network_RX=float(row[4]),
                Network_TX=float(row[5]),
                Inlet_Temperature=float(row[6]),
                CPU1_Temperature=float(row[7]),
                CPU2_Temperature=float(row[8]),
                Fan_speed1=float(row[9]),
                Fan_speed2=float(row[10]),
                Fan_speed3=float(row[11]),
                Fan_speed4=float(row[12]),
                Ram=float(row[13]),
                Ram_Used=float(row[14]),
                No_Of_Running_vms=float(row[15]),
                CPU_cores=float(row[16]),
                CPU_cores_used=float(row[17])
            )
            data = json.dumps(reading.__dict__)
            client.publish(pub_topic, data)
            
            time.sleep(10) #600s=10min


@app.route('/')
def index():
    return 'Sensor  microservice'


if __name__ == '__main__':

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish

    client.connect(broker_address, broker_port, 60)
    client.loop_start()

    threading.Thread(target=simulate_sensor_data, args=(client,"")).start()

    app.run()
