from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return "Varta Backend Running 🚀"


# Login API
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


# Signup API
@app.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    return jsonify({
        "status": "success",
        "message": f"{username} created successfully"
    })


# Important for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
