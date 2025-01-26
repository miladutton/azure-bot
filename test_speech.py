import azure.cognitiveservices.speech as speechsdk
import os

speech_key = os.getenv("AZURE_SPEECH_KEY")
service_region = os.getenv("AZURE_SPEECH_REGION")


def test_speech_synthesis():
    # Replace with your Azure Speech service credentials
    speech_key = "YOUR_AZURE_SPEECH_KEY"
    service_region = "YOUR_AZURE_REGION"

    # Initialize speech configuration
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Set the audio output to null (no playback, just test the service)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Text to synthesize
    text = "Testing Azure Speech Service on Heroku."

    # Perform speech synthesis
    print("Starting speech synthesis...")
    result = synthesizer.speak_text_async(text).get()

    # Handle the result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized successfully.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")

if __name__ == "__main__":
    test_speech_synthesis()
