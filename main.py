import os
import azure.cognitiveservices.speech as speechsdk
from bot_logic.professional_bot import ProfessionalBot
from bot_logic.moderate_bot import ModerateBot
from bot_logic.casual_bot import CasualBot
from speech.text_to_speech import speak_text
from speech.speech_to_text import recognize_speech


def run_professional_bot():
    return run_bot("professional")


def run_moderate_bot():
    return run_bot("moderate")


def run_friendly_bot():
    return run_bot("friendly")


def run_bot(agent_type):
    """
    Runs the selected bot based on agent_type ('professional', 'moderate', 'friendly').
    Continuously listens for user responses and prints them to the terminal.
    """
    # Initialize Azure Speech SDK
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_REGION")

    if not speech_key or not region:
        return {"error": "Azure Speech Key or Region is not set."}

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)

    # Select the appropriate bot and settings
    if agent_type == "professional":
        bot = ProfessionalBot()
        style, pitch, rate = "newscast", "0%", "0.9"
    elif agent_type == "moderate":
        bot = ModerateBot()
        style, pitch, rate = "calm", "+2%", "1.0"
    elif agent_type == "friendly":
        bot = CasualBot()
        style, pitch, rate = "friendly", "+5%", "1.2"
    else:
        return {"error": "Invalid agent type. Choose 'professional', 'moderate', or 'friendly'."}

    # Initialize session
    questions_and_responses = []
    speak_text(
        speech_config,
        "Hello, welcome to this session. I will ask you some questions.",
        style=style, pitch=pitch, rate=rate,
    )

    while True:
        # Get the next question from the bot
        question = bot.get_next_question()
        if question is None:
            speak_text(
                speech_config,
                "Thank you for completing this session. Your responses are greatly appreciated.",
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

    return {"questions_and_responses": questions_and_responses}


if __name__ == "__main__":
    # Local testing
    agent_type = input("Choose agent type (professional, moderate, friendly): ").strip().lower()

    if agent_type in ["professional", "moderate", "friendly"]:
        result = run_bot(agent_type)
        print(result)
    else:
        print("Invalid selection. Please choose from 'professional', 'moderate', or 'friendly'.")
