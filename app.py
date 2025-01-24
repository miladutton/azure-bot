from flask import Flask, request, jsonify, render_template
from main import run_professional_bot, run_moderate_bot, run_friendly_bot

app = Flask(__name__, template_folder='templates')  # Ensure 'templates' folder is correctly set

@app.route("/")
def home():
    return render_template("index.html")  # Render the HTML page

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
