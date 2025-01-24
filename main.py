import os
import azure.cognitiveservices.speech as speechsdk
from bot_logic.professional_bot import ProfessionalBot
from bot_logic.moderate_bot import ModerateBot
from bot_logic.casual_bot import CasualBot
from speech.text_to_speech import speak_text
from speech.speech_to_text import recognize_speech

def run_agent(agent_type, bot, speech_config, style, pitch, rate):
    """
    Runs a single agent session and collects user responses.
    Returns session data.
    """
    questions_and_responses = []
    speak_text(
        speech_config,
        f"Hello, welcome to the {agent_type} agent session. I will ask you some questions.",
        style=style, pitch=pitch, rate=rate,
    )

    while True:
        # Get the next question from the bot
        question = bot.get_next_question()
        if question is None:
            speak_text(
                speech_config,
                f"Thank you for completing the {agent_type} agent session. Your responses are greatly appreciated.",
                style=style, pitch=pitch, rate=rate,
            )
            break

        # Speak the question
        speak_text(speech_config, question, style=style, pitch=pitch, rate=rate)
        print(f"Asking: {question}")  # Debugging output

        # Listen for user response
        user_response = recognize_speech()
        if not user_response:
            user_response = "No response detected."
            speak_text(speech_config, "Sorry, I didn't catch that.", style=style, pitch=pitch, rate=rate)

        # Store the question and response
        questions_and_responses.append({"question": question, "response": user_response})
        print(f"User said: {user_response}")  # Output user response to terminal

    # Return session data without follow-up responses
    return {
        "agent_type": agent_type,
        "questions_and_responses": questions_and_responses,
    }

def run_all_agents():
    """
    Runs all agents (Professional, Moderate, Friendly) sequentially and collects session data.
    """
    # Initialize Azure Speech SDK
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_REGION")

    if not speech_key or not region:
        return {"error": "Azure Speech Key or Region is not set."}

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)

    # Define agents and their settings
    agents = [
        {"type": "professional", "bot": ProfessionalBot(), "style": "newscast", "pitch": "0%", "rate": "0.9"},
        {"type": "moderate", "bot": ModerateBot(), "style": "calm", "pitch": "+2%", "rate": "1.0"},
        {"type": "friendly", "bot": CasualBot(), "style": "friendly", "pitch": "+5%", "rate": "1.2"},
    ]

    # Run each agent and collect responses
    all_sessions = []
    for agent in agents:
        session_data = run_agent(
            agent["type"], agent["bot"], speech_config, agent["style"], agent["pitch"], agent["rate"]
        )
        all_sessions.append(session_data)

    return all_sessions

if __name__ == "__main__":
    # Run all agents sequentially
    results = run_all_agents()

    # Save or print the results for debugging
    print("All sessions completed:")
    for result in results:
        print(result)
