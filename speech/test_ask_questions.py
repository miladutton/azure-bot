import sys
import os

print("Current sys.path:")
print("\n".join(sys.path))

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
print("\nUpdated sys.path:")
print("\n".join(sys.path))

from bot_logic.professional_bot import ProfessionalBot
from speech.speech_to_text import recognize_speech


from speech.text_to_speech import speak_text  # Ensure this module works

questions = [
    "Could you describe what a typical breakfast entails for you, if applicable?",
    "Do you have particular foods that you prefer to cook or prepare personally?",
    "Are you currently pursuing any specific health-related objectives?",
]

def ask_questions():
    for question in questions:
        print(f"Asking: {question}")
        speak_text(question)  # This uses Azure's text-to-speech to ask the question

if __name__ == "__main__":
    ask_questions()

