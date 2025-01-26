# /mnt/data/main.py
import time
import os
import azure.cognitiveservices.speech as speechsdk
from bot_logic.professional_bot import ProfessionalBot
from bot_logic.moderate_bot import ModerateBot
from bot_logic.casual_bot import CasualBot
from speech.text_to_speech import speak_text
from speech.speech_to_text import recognize_speech

# Initialize Azure Speech SDK
speech_key = os.getenv("AZURE_SPEECH_KEY")
region = os.getenv("AZURE_REGION")
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)


def run_agent(agent_type, bot, speech_config, style, pitch, rate, delay=8):
    """
    Runs the agent session and handles the conversation with a configurable delay.
    """
    questions_and_responses = []

    # Start the session with a greeting
    speak_text(
        speech_config,
        f"Hello, welcome to the {agent_type} agent session. I will ask you a few questions.",
        style=style,
        pitch=pitch,
        rate=rate
    )

    while True:
        question = bot.get_next_question()
        if question is None:
            speak_text(
                speech_config,
                f"Thank you for completing the {agent_type} agent session. Your responses are greatly appreciated.",
                style=style,
                pitch=pitch,
                rate=rate
            )
            break

        # Speak the question dynamically
        speak_text(
            speech_config,
            question,
            style=style,
            pitch=pitch,
            rate=rate
        )

        # Add a delay before capturing user input
        time.sleep(delay)

        # Recognize user’s response
        user_response = recognize_speech()
        if not user_response:
            speak_text(
                speech_config,
                "Sorry, I didn’t catch that. Could you repeat?",
                style=style,
                pitch=pitch,
                rate=rate
            )
            continue

        questions_and_responses.append({"question": question, "response": user_response})

    return {"agent_type": agent_type, "questions_and_responses": questions_and_responses}


# Mock speech recognition function for development
def recognize_speech():
    """
    Simulates user speech recognition for development purposes.
    """
    # Simulate a user response
    return "This is a simulated response."
