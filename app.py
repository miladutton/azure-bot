from flask import Flask, request, jsonify, render_template
import os
from main import run_professional_bot, run_moderate_bot, run_friendly_bot

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # Serve the HTML page

@app.route("/bot", methods=["POST"])
def bot_interaction():
    agent_type = request.json.get("agent_type", "professional")
    
    if agent_type == "professional":
        run_professional_bot()
    elif agent_type == "moderate":
        run_moderate_bot()
    elif agent_type == "friendly":
        run_friendly_bot()
    else:
        return jsonify({"error": "Invalid agent type. Choose 'professional', 'moderate', or 'friendly'."}), 400
    
    return jsonify({"message": f"Bot session completed for agent type '{agent_type}'."})

if __name__ == "__main__":
    app.run(debug=True)
