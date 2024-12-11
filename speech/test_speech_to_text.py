import os
import azure.cognitiveservices.speech as speechsdk

def test_speech_to_text():
    # Retrieve Azure credentials
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_REGION")

    if not speech_key or not region:
        print("Azure Speech Key or Region is not set.")
        return

    # Configure the Azure Speech SDK
    speech_config = speechsdk.SpeechConfig(subscription=os.getenv("AZURE_SPEECH_KEY"), region=os.getenv("AZURE_REGION"))

    # Create a Speech Recognizer
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    print("Say something into your microphone...")

    # Perform speech recognition
    result = recognizer.recognize_once()

    # Check result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized Speech: {result.text}")
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized.")
    else:
        print(f"Speech-to-Text failed. Reason: {result.reason}")

test_speech_to_text()
