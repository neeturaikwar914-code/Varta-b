import sqlite3
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)

# database connect
def get_db():
    return sqlite3.connect("varta.db")

# signup
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data["username"]
    password = data["password"]

    db = get_db()
    cur = db.cursor()

    try:
        cur.execute(
        "INSERT INTO users (username,password_hash) VALUES (?,?)",
        (username,password))
        db.commit()

        return jsonify({"status":"account created"})
    except:
        return jsonify({"status":"username exists"})

# login
@app.route("/login", methods=["POST"])
def login():

    data = request.json
    username = data["username"]
    password = data["password"]

    db = get_db()
    cur = db.cursor()

    cur.execute(
    "SELECT id FROM users WHERE username=? AND password_hash=?",
    (username,password))

    user = cur.fetchone()

    if user:

        token = str(uuid.uuid4())

        cur.execute(
        "INSERT INTO sessions (user_id,session_token) VALUES (?,?)",
        (user[0],token))

        db.commit()

        return jsonify({"token":token})

    return jsonify({"error":"invalid login"})

app.run(host="0.0.0.0", port=10000)
