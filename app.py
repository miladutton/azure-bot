from flask import Flask, jsonify, render_template
from main import run_agent
from bot_logic.professional_bot import ProfessionalBot
from bot_logic.moderate_bot import ModerateBot
from bot_logic.casual_bot import CasualBot
import os
import azure.cognitiveservices.speech as speechsdk

app = Flask(__name__, template_folder="templates")

# Initialize Azure Speech SDK
speech_key = os.getenv("AZURE_SPEECH_KEY")
region = os.getenv("AZURE_REGION")
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)

# Define agents in a hard-coded order
agents = [
    {"type": "professional", "bot": ProfessionalBot(), "style": "newscast", "pitch": "0%", "rate": "0.9"},
    {"type": "moderate", "bot": ModerateBot(), "style": "calm", "pitch": "+2%", "rate": "1.0"},
    {"type": "friendly", "bot": CasualBot(), "style": "friendly", "pitch": "+5%", "rate": "1.2"},
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/bot", methods=["POST"])
def handle_agent_session():
    # Loop through the hard-coded agents
    for agent in agents:
        agent_type = agent["type"]
        bot = agent["bot"]
        try:
            # Run the session for the current agent
            session_data = run_agent(
                agent_type=agent_type,
                bot=bot,
                speech_config=speech_config,
                style=agent["style"],
                pitch=agent["pitch"],
                rate=agent["rate"]
            )
            # Log or process session data as needed
            print(f"Completed session for {agent_type} agent.")
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # All agents have been processed
    return jsonify({"message": "All agents have been processed successfully."}), 200

if __name__ == "__main__":
    app.run(debug=True)
