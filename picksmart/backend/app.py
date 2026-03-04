from flask import Flask, request, jsonify, session
from flask_cors import CORS
import uuid
import os
from conversation_manager import ConversationManager

app = Flask(__name__)
app.secret_key = "smartpick_secret_key"
CORS(app)

managers = {}

def get_manager():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())

    session_id = session["session_id"]

    if session_id not in managers:
        managers[session_id] = ConversationManager("phones.json")

    return managers[session_id]


@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    manager = get_manager()
    response = manager.handle_message(user_message)
    return jsonify(response)


@app.route("/reset", methods=["POST"])
def reset():
    session_id = session.get("session_id")
    if session_id and session_id in managers:
        managers[session_id] = ConversationManager("phones.json")
    return jsonify({"status": "reset"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
