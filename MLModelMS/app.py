from flask import Flask, jsonify, request
import pickle,json
import numpy as np

app = Flask(__name__)

model_pkl_file1 = "cpu_load_model.pkl"
with open(model_pkl_file1, 'rb') as file:  
    cpu_load_model = pickle.load(file)
scaler_pkl_file1 = "cpu_scaler.pkl"
with open(scaler_pkl_file1, 'rb') as file:  
    cpu_scaler = pickle.load(file)

model_pkl_file2 = "power_model.pkl"
with open(model_pkl_file2, 'rb') as file:  
    power_consp_model = pickle.load(file)
scaler_pkl_file2 = "power_scaler.pkl"
with open(scaler_pkl_file2, 'rb') as file:  
    power_scaler = pickle.load(file)

def preprocess_message(payload, choice):
    if choice=='cpu':
        exclude_fields = ["Series", "Time", "CPU_Load"]
    else:
        exclude_fields = ["Series", "Time", "Power"]

    data = [value for key, value in payload.items() if key not in exclude_fields]
    npdata = np.array(data) #.reshape(1, -1)

    time_value = payload.get("Time", None)
    if choice=='cpu':
        return cpu_scaler.transform([npdata]), time_value
    else:
        return power_scaler.transform([npdata]),  time_value

@app.route('/predict/cpuload', methods=['POST'])
def predict_cpu_load():
    message_data = request.get_json()
    processed_data, time_value = preprocess_message(message_data, "cpu")

    cpu_load_prediction = cpu_load_model.predict(processed_data)
    print("Predicted data cpu ",cpu_load_prediction[0][0])

    return jsonify({
        "cpu_load_prediction": cpu_load_prediction[0][0], 
        "time_value": time_value
    }), 200

@app.route('/predict/power', methods=['POST'])
def predict_power():
    message_data = request.get_json()
    processed_data, time_value = preprocess_message(message_data, "power")
    power_consp_prediction = power_consp_model.predict(processed_data)
    print("Predicted data power",power_consp_prediction[0][0])

    return jsonify({
        "power_prediction": power_consp_prediction[0][0], 
        "time_value": time_value
    }), 200


@app.route('/')
def index():
    return 'MLModel  microservice'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005)

