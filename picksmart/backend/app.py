from flask import Flask, request, jsonify
from flask_cors import CORS
from conversation_manager import ConversationManager
import os

app = Flask(__name__)
CORS(app)

# In-memory session store
managers = {}

def get_manager(session_id):
    if session_id not in managers:
        managers[session_id] = ConversationManager("phones.json")
    return managers[session_id]


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    session_id = data.get("session_id")

    if not session_id:
        return jsonify({"error": "Missing session_id"}), 400

    manager = get_manager(session_id)
    response = manager.handle_message(user_message)
    return jsonify(response)


@app.route("/reset", methods=["POST"])
def reset():
    data = request.json
    session_id = data.get("session_id")

    if session_id and session_id in managers:
        managers[session_id] = ConversationManager("phones.json")

    return jsonify({"status": "reset"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
