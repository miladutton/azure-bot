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

def run_agent(agent_type, bot, speech_config, style, pitch, rate):
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

        # Recognize user's response
        user_response = recognize_speech()
        if not user_response:
            speak_text(
                speech_config,
                "Sorry, I didn't catch that. Could you repeat?",
                style=style,
                pitch=pitch,
                rate=rate
            )
            continue

        questions_and_responses.append({"question": question, "response": user_response})

    return {"agent_type": agent_type, "questions_and_responses": questions_and_responses}

# Mock speech recognition function
def recognize_speech():
    # Simulate a user response
    return "This is a simulated response."
