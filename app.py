from flask import Flask, jsonify, render_template
from main import run_all_agents  # Import the new function for running all agents sequentially

app = Flask(__name__, template_folder='templates')  # Ensure 'templates' folder is correctly set

@app.route("/")
def home():
    return render_template("index.html")  # Render the HTML page

@app.route("/bot", methods=["POST"])
def bot_interaction():
    """
    Handles the interaction with all agents sequentially and returns the results.
    """
    try:
        # Run all agents sequentially
        response = run_all_agents()
        return jsonify(response)  # Return the combined results as JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error message if something goes wrong

if __name__ == "__main__":
    app.run(debug=True)
