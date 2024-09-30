from flask import Flask, request, jsonify
import requests,os
from flask_socketio import SocketIO,emit,send
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')
thread = None
clients = 0

DASHBOARD_MS_URL = os.getenv('DASHBOARD_MS_URL')
AUTH_MS_URL=os.getenv('AUTH_MS_URL')


@socketio.on('connect')
def test_connect():
    global clients
    clients += 1
    print('Client connected')


@app.route('/login', methods=["POST"])
def login():
    print("Client tried to login.")
    auth = request.authorization 
    basicAuth=None
    if auth:
        basicAuth=(auth.username, auth.password)
    try:
        response = requests.post(f"{AUTH_MS_URL}/login", auth=basicAuth)
        if response.status_code == 200:
            print("Client successfully managed to login.")
            return jsonify({"token":response.text}),response.status_code
        else:
            print("Client did not manage to login.")
            return jsonify({"error": response.text}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/signup', methods=["POST"])
def signup():
    print("Client tried to signup.")
    data=request.json
    try:
        response = requests.post(f"{AUTH_MS_URL}/signup",json=data)
        if response.status_code == 201:
            print("Client successfully managed to signup.")
            return jsonify({"message":response.text}),response.status_code
        else:
            print("Client did not manage to signup.")
            return jsonify({"error": response.text}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


@app.route('/notify', methods=['POST']) #notify stize od CommandMS
def notify_command_ms():
    print("Received notification from CommandMS.")
    data = request.json
    if not data:
        print("No data provided")
        return jsonify({"error": "No data provided"}), 500
        
    socketio.emit('data-notf', data) 
    print("Passing the notification to the client.")
    return jsonify({"message":"Client notified."}),200


@app.route('/snapshot', methods=['GET']) #history stize od clienta
def get_history_data():
    print("Client requested snapshot.")
    if not "Authorization" in request.headers:
        return jsonify({"error":"Missing authoritazion credentials"}), 401
    #check if the client has a valid token
    access, err = validate_token(request)
    
    if err:
        return jsonify({"error": err}), 500

    try:
        response = requests.get(f"{DASHBOARD_MS_URL}/get_snapshot")
        print("Sent the link for snapshot to client.")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500


def validate_token(request):
    token = request.headers["Authorization"]
    if not token:
        return None, ("Missing credentials in validate token", 401)

    response = requests.post(f"{AUTH_MS_URL}/validate",headers={"Authorization": token},
    )

    if response.status_code == 200:
        return response.text, None      #access,err
    else:
        return None, (response.text, response.status_code) #access,err

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
