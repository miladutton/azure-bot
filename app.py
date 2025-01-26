from flask import Flask, jsonify, render_template, request
from main import run_agent  # Import the reusable run_agent function
from bot_logic.professional_bot import ProfessionalBot
from bot_logic.moderate_bot import ModerateBot
from bot_logic.casual_bot import CasualBot
import os
import azure.cognitiveservices.speech as speechsdk

app = Flask(__name__, template_folder='templates')  # Point to the templates folder for HTML rendering

# Initialize Azure Speech SDK
speech_key = os.getenv("AZURE_SPEECH_KEY")
region = os.getenv("AZURE_REGION")
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)

# Define agents and their settings
agents = [
    {"type": "professional", "bot": ProfessionalBot(), "style": "newscast", "pitch": "0%", "rate": "0.9"},
    {"type": "moderate", "bot": ModerateBot(), "style": "calm", "pitch": "+2%", "rate": "1.0"},
    {"type": "friendly", "bot": CasualBot(), "style": "friendly", "pitch": "+5%", "rate": "1.2"},
]

# Shared state to track the current agent index
current_agent_index = 0

@app.route("/")
def home():
    return render_template("index.html")  # Render the homepage with the start button

@app.route("/bot", methods=["POST"])
def handle_agent_session():
    global current_agent_index

    # Check if we've exhausted all agents
    if current_agent_index >= len(agents):
        return jsonify({"error": "All agents have been processed."}), 400

    # Get the current agent
    agent = agents[current_agent_index]
    agent_type = agent["type"]
    bot = agent["bot"]

    try:
        # Run the agent session
        session_data = run_agent(
            agent_type,
            bot,
            speech_config,
            agent["style"],
            agent["pitch"],
            agent["rate"]
        )
        return jsonify(session_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/next-agent", methods=["POST"])
def move_to_next_agent():
    global current_agent_index

    # Increment the agent index
    current_agent_index += 1

    # Check if there are more agents
    if current_agent_index >= len(agents):
        return jsonify({"message": "All agents have been processed."}), 200

    return jsonify({"message": "Moved to the next agent."}), 200


if __name__ == "__main__":
    app.run(debug=True)
