import os
import azure.cognitiveservices.speech as speechsdk
from bot_logic.professional_bot import ProfessionalBot
from bot_logic.moderate_bot import ModerateBot
from bot_logic.casual_bot import CasualBot
from speech.text_to_speech import speak_text
from speech.speech_to_text import recognize_speech
import time

def run_professional_bot():
    run_bot("professional")

def run_moderate_bot():
    run_bot("moderate")

def run_friendly_bot():
    run_bot("friendly")

def run_bot(agent_type):
    """
    Runs the selected bot based on agent_type ('professional', 'moderate', 'friendly').
    """
    # Initialize Azure Speech SDK
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_REGION")

    print(f"Speech Key: {speech_key}")  # Debugging print to check if the key is correct
    print(f"Region: {region}")  # Debugging print to check if the region is correct

    if not speech_key or not region:
        print("Azure Speech Key or Region is not set.")
        return

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
    print("Azure Speech Config initialized successfully!")  # Confirm that Speech SDK is initialized


    # Select the appropriate bot
    if agent_type == "professional":
        bot = ProfessionalBot()
        style, pitch, rate = "neutral", "0%", "0.9"  # Professional tone
        pauses = {"commas": 0.2, "periods": 0.4}  # Deliberate pauses
        volume = "medium"
        articulation = "crisp"
        vocabulary = ["formal", "business-oriented"]
        sentence_end = "neutral"
        emotion = "minimal"

    elif agent_type == "moderate":
        bot = ModerateBot()
        style, pitch, rate = "calm", "+10%", "1.0"  # Moderate tone
        pauses = {"commas": 0.15, "periods": 0.3}  # Balanced pauses
        volume = "medium-soft"
        articulation = "smooth"
        vocabulary = ["simple", "accessible"]
        sentence_end = "balanced"
        emotion = "subtle"

    elif agent_type == "friendly":
        bot = CasualBot()
        style, pitch, rate = "cheerful", "+20%", "1.2"  # Friendly tone
        pauses = {"commas": 0.1, "periods": 0.2}  # Shorter pauses
        volume = "medium-loud"
        articulation = "relaxed"
        vocabulary = ["informal", "friendly", "light humor"]
        sentence_end = "upbeat"
        emotion = "expressive"

    else:
        raise ValueError("Invalid agent type. Choose 'professional', 'moderate', or 'friendly'.")


    # Start the session with a greeting
    print("before") 
    speak_text(speech_config,"Hello, welcome to this session. I will ask you some questions.",
               style=style, pitch=pitch, rate=rate)
    print("after")

    while True:
        # Ask the next question
        print("Asking next question...")  # Debugging print to check if loop is running
        question = bot.get_next_question()  # Assuming your bot logic provides these questions
        if question is None:
            print("No more questions.")  # Debugging output to confirm end of session
            speak_text(speech_config, "Thank you for completing this session. Your responses are greatly appreciated.",
                       style=style, pitch=pitch, rate=rate)
            break

        # Speak the question
        print(f"Asking: {question}")  # Debugging output to ensure it's being triggered
        speak_text(speech_config, question, style=style, pitch=pitch, rate=rate)

        # Capture user response using Speech-to-Text
        print("Listening for user response...")  # Debugging output
        user_response = recognize_speech()

        if not user_response:
            print("No response detected.")  # Debugging output if no response is detected
            speak_text(speech_config, "Sorry, I didn't catch that. Could you please repeat?", style=style, pitch=pitch, rate=rate)
        elif user_response.lower() in ["i don't know", "not sure"]:
            print("User responded with unclear input.")  # Debugging output for unclear input
            error_message = bot.handle_error()
            speak_text(speech_config, error_message, style=style, pitch=pitch, rate=rate)
        else:
            print(f"User said: {user_response}")  # Debugging output to print the user's response
            speak_text(speech_config, "Thank you for your response.", style=style, pitch=pitch, rate=rate)

def safe_recognize_speech():
    retries = 3
    for attempt in range(retries):
        try:
            print(f"Attempt {attempt + 1} to recognize speech...")  # Debugging output for retry attempt
            user_response = recognize_speech()
            if user_response:
                return user_response
            else:
                print("No speech detected, retrying...")  # Debugging output if speech not detected
        except Exception as e:
            print(f"Error on attempt {attempt + 1}: {e}")  # Debugging output for error during recognition
        time.sleep(2)  # Wait for 2 seconds before retrying
    return None  # Return None if all attempts fail

if __name__ == "__main__":
    agent_type = input("Choose agent type (professional, moderate, friendly): ").strip().lower()

    # Based on the agent type, call the appropriate main function
    if agent_type == "professional":
        run_professional_bot()
    elif agent_type == "moderate":
        run_moderate_bot()
    elif agent_type == "friendly":
        run_friendly_bot()
    else:
        print("Invalid selection. Please choose from 'professional', 'moderate', or 'friendly'.")