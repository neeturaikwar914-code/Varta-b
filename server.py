from flask import Flask, request, jsonify

app = Flask(__name__)

# Home route (backend check)
@app.route("/")
def home():
    return "Varta Backend Running 🚀"


# Login API
@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    # demo login
    if username == "admin" and password == "1234":
        return jsonify({
            "status": "success",
            "message": "Login successful"
        })
    else:
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
        "message": f"User {username} created successfully"
    })


# Chat test API
@app.route("/chat", methods=["GET"])
def chat():

    messages = [
        {"user": "Rahul", "message": "Hello"},
        {"user": "Aman", "message": "Hi bro"},
        {"user": "Riya", "message": "Good morning"}
    ]

    return jsonify(messages)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
