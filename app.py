from flask import Flask, jsonify, render_template, request, session, send_file
from flask_session import Session
from bot_logic.professional_bot import ProfessionalBot
from bot_logic.moderate_bot import ModerateBot
from bot_logic.casual_bot import CasualBot
import os
import azure.cognitiveservices.speech as speechsdk

app = Flask(__name__, template_folder="templates")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "default-secret-key")
app.config['SESSION_TYPE'] = 'filesystem'  # Use a filesystem-based session store
Session(app)

# Azure Speech SDK Configuration
speech_key = os.getenv("AZURE_SPEECH_KEY")
region = os.getenv("AZURE_REGION")
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
audio_config = speechsdk.audio.AudioOutputConfig(filename="output.wav")  # Saves speech output

# Define agents with different styles, pitch, and rate, but the same female voice
agents = [
    {"type": "professional", "bot": ProfessionalBot(), "style": "newscast", "pitch": "0%", "rate": "0.9"},
    {"type": "moderate", "bot": ModerateBot(), "style": "calm", "pitch": "+2%", "rate": "1.0"},
    {"type": "friendly", "bot": CasualBot(), "style": "friendly", "pitch": "+5%", "rate": "1.2"},
]

# Set a single default **female** voice for all agents
DEFAULT_VOICE = "en-US-JennyNeural"  # Female voice

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


# ✅ **FIXED: generate_speech() is now correctly placed!**
@app.route("/generate-speech", methods=["POST"])
def generate_speech():
    try:
        data = request.get_json(force=True)
        text = data.get("text", "Hello! This is Azure Speech.")

        # Get the current agent's settings
        current_agent_index = session.get("current_agent_index", 0)
        agent = agents[current_agent_index]

        style = agent["style"]
        pitch = agent["pitch"]
        rate = agent["rate"]

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Generate SSML with style, pitch, and rate
        ssml = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts' xml:lang='en-US'>
            <voice name='{DEFAULT_VOICE}'>
                <mstts:express-as style='{style}'>
                    <prosody pitch='{pitch}' rate='{rate}'>
                        {text}
                    </prosody>
                </mstts:express-as>
            </voice>
        </speak>
        """

        print("🔍 Generated SSML:\n", ssml)  # Debugging

        # Use the same voice for all agents
        speech_config.speech_synthesis_voice_name = DEFAULT_VOICE

        # Generate speech using SSML
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        result = synthesizer.speak_ssml_async(ssml).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return send_file("output.wav", mimetype="audio/wav")
        else:
            print("❌ Speech synthesis failed:", result.reason)
            return jsonify({"error": "Speech synthesis failed"}), 500

    except Exception as e:
        print("🔥 Error in speech synthesis:", e)
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
