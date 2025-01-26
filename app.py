from flask import Flask, jsonify, render_template, request, session
from flask_session import Session
from main import run_agent
from bot_logic.professional_bot import ProfessionalBot
from bot_logic.moderate_bot import ModerateBot
from bot_logic.casual_bot import CasualBot
import os
import azure.cognitiveservices.speech as speechsdk

app = Flask(__name__, template_folder="templates")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default-secret-key")
app.config['SESSION_TYPE'] = 'filesystem'  # Use a filesystem-based session store
Session(app)

# Initialize Azure Speech SDK
speech_key = os.getenv("AZURE_SPEECH_KEY")
region = os.getenv("AZURE_REGION")
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)

# Define agents in a fixed order
agents = [
    {"type": "professional", "bot": ProfessionalBot(), "style": "newscast", "pitch": "0%", "rate": "0.9"},
    {"type": "moderate", "bot": ModerateBot(), "style": "calm", "pitch": "+2%", "rate": "1.0"},
    {"type": "friendly", "bot": CasualBot(), "style": "friendly", "pitch": "+5%", "rate": "1.2"},
]


@app.route("/")
def home():
    # Reset session when loading the home page
    session["current_agent_index"] = 0
    return render_template("index.html")


@app.route("/bot", methods=["POST"])
def handle_agent_session():
    # Retrieve the current agent index
    current_agent_index = session.get("current_agent_index", 0)

    # Check if all agents have been processed
    if current_agent_index >= len(agents):
        return jsonify({"message": "All agents have been processed."}), 200

    # Get the current agent
    agent = agents[current_agent_index]

    try:
        # Run the session for the current agent
        run_agent(
            agent_type=agent["type"],
            bot=agent["bot"],
            speech_config=speech_config,
            style=agent["style"],
            pitch=agent["pitch"],
            rate=agent["rate"],
            delay=10  # Keep the 10-second delay between questions
        )
        return jsonify({
            "message": "The session is complete. Please proceed to the follow-up questions.",
            "agent_type": "agent"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/submit-follow-up", methods=["POST"])
def handle_follow_up_questions():
    # Retrieve the current agent index from session
    current_agent_index = session.get("current_agent_index", 0)

    # Collect follow-up responses (frontend sends these)
    data = request.get_json()
    print(f"Received follow-up responses for agent {agents[current_agent_index]['type']}: {data}")

    # Increment the agent index and update the session
    current_agent_index += 1
    session["current_agent_index"] = current_agent_index

    # Check if there are remaining agents
    if current_agent_index < len(agents):
        return jsonify({"message": "Proceeding to the next agent."}), 200
    else:
        return jsonify({"message": "All agents and follow-up questions have been completed."}), 200


if __name__ == "__main__":
    app.run()  # Remove `debug=True`
