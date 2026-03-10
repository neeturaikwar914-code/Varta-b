from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

# CORS allow
CORS(app)

@app.route("/")
def home():
    return "Varta Backend Running 🚀"


@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if username == "admin" and password == "1234":
        return jsonify({
            "status": "success",
            "message": "Login successful"
        })

    return jsonify({
        "status": "error",
        "message": "Wrong username or password"
    })


@app.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    return jsonify({
        "status": "success",
        "message": f"{username} created successfully"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
