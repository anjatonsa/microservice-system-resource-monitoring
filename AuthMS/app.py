import jwt, datetime, os, time, threading
from flask import Flask, request,jsonify
from flask_mysqldb import MySQL


server = Flask(__name__)
mysql = MySQL(server)



server.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
server.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
server.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
server.config['MYSQL_DB'] = os.getenv('MYSQL_DATABASE')


@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "Missing credentials", 401

    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT username, password FROM user WHERE username=%s", (auth.username,)
    )
    if res > 0:
        user_row = cur.fetchone()
        username = user_row[0]
        password = user_row[1]
        cur.close()
        if auth.username !=username or auth.password != password:
            return "Invalid credentials", 401
        else:
            return createJWT(auth.username, os.getenv("JWT_SECRET"), True)
    else:
        return "Invalid credentials", 404


@server.route("/signup", methods=["POST"])  
def signup():
    data=request.json
    email=data.get("email")
    username=data.get("username")
    password=data.get("password")

    if not email or not username or not password:
        return "Missing data", 400
    
    try:
        cur = mysql.connection.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS user (
                        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        email VARCHAR(255) NOT NULL UNIQUE,
                        username VARCHAR(255) NOT NULL UNIQUE,
                        password VARCHAR(255) NOT NULL
                    );''')
        cur.execute(
            "INSERT INTO user (email, username, password) VALUES (%s, %s, %s)",
            (email, username, password)
        )
        mysql.connection.commit()
        cur.close()
        return "User created successfully", 201
    except Exception as e:
        return str(e), 500



def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz,
        },
        secret,
        algorithm="HS256",
    )

@server.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT DATABASE()")
    database_name = cur.fetchone()
    cur.close()
    return jsonify({'message': f'Connected to {database_name[0]}'})

@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401

    encoded_jwt = encoded_jwt.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, os.getenv ("JWT_SECRET"), algorithms=["HS256"]
        )
    except:
        return "not authorized", 403

    return decoded, 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5004)