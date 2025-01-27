from flask import Flask, jsonify, render_template, request, session
from flask_session import Session
from bot_logic.professional_bot import ProfessionalBot
from bot_logic.moderate_bot import ModerateBot
from bot_logic.casual_bot import CasualBot
import os

app = Flask(__name__, template_folder="templates")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default-secret-key")
app.config['SESSION_TYPE'] = 'filesystem'  # Use a filesystem-based session store
Session(app)

# Define agents in a fixed order
agents = [
    {"type": "professional", "bot": ProfessionalBot()},
    {"type": "moderate", "bot": ModerateBot()},
    {"type": "friendly", "bot": CasualBot()},
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
        # Get questions from the current agent
        questions = []
        while True:
            question = agent["bot"].get_next_question()
            if question is None:
                break
            questions.append(question)

        return jsonify({
            "message": "The session is ready to begin.",
            "agent_type": agent["type"],
            "questions": questions
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/submit-follow-up", methods=["POST"])
def handle_follow_up_questions():
    # Retrieve the current agent index from session
    current_agent_index = session.get("current_agent_index", 0)

    # Collect follow-up responses
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
    app.run(debug=True)