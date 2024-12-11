from flask import Flask, request, jsonify
from main import run_bot, safe_recognize_speech

app = Flask(__name__)

# Root route to avoid 404 error
@app.route('/')
def home():
    return "Welcome to My Flask App!"  # Simple message to verify the app is running

# Serve bot interactions
@app.route('/run_bot', methods=['POST'])
def run_bot_endpoint():
    """
    Run the bot session based on the agent type.
    """
    data = request.json
    agent_type = data.get("agent_type", "").lower()

    if agent_type not in ["professional", "moderate", "friendly"]:
        return jsonify({"error": "Invalid agent type. Choose 'professional', 'moderate', or 'friendly'."}), 400

    try:
        # Call the run_bot function from main.py
        response = run_bot(agent_type)
        return jsonify({"status": "success", "response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Speech recognition endpoint
@app.route('/speech_to_text', methods=['POST'])
def speech_to_text_endpoint():
    """
    Use the safe_recognize_speech function for speech-to-text.
    """
    try:
        user_response = safe_recognize_speech()
        if not user_response:
            return jsonify({"error": "No speech detected. Please try again."}), 400
        return jsonify({"text": user_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)  # Change to port 5001 or any available port
