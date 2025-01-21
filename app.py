from flask import Flask, request, jsonify
from main import run_professional_bot, run_moderate_bot, run_friendly_bot

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Bot Application!"

@app.route("/bot", methods=["POST"])
def bot_interaction():
    agent_type = request.json.get("agent_type", "professional")  # Get the agent type

    # Call the appropriate bot function
    if agent_type == "professional":
        response = run_professional_bot()
    elif agent_type == "moderate":
        response = run_moderate_bot()
    elif agent_type == "friendly":
        response = run_friendly_bot()
    else:
        return jsonify({"error": "Invalid agent type. Choose 'professional', 'moderate', or 'friendly'."}), 400

    return jsonify(response)  # Return the bot's output as JSON


if __name__ == "__main__":
    app.run(debug=True)
