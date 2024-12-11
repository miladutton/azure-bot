import os
import azure.cognitiveservices.speech as speechsdk

def test_text_to_speech():
    # Retrieve Azure credentials
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_REGION")

    if not speech_key or not region:
        print("Azure Speech Key or Region is not set.")
        return

    # Configure the Azure Speech SDK
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)

    # Text to convert to speech
    text = "Hello! This is a test of the Azure Text-to-Speech service."
    print(f"Converting the following text to speech: '{text}'")

    # Create a Speech Synthesizer
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Synthesize speech
    result = synthesizer.speak_text_async(text).get()

    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Text-to-Speech succeeded!")
    else:
        print(f"Text-to-Speech failed. Reason: {result.reason}")

test_text_to_speech()
