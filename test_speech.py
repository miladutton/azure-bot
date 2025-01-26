import azure.cognitiveservices.speech as speechsdk

def test_speech_synthesis():
    import os
    # Replace with your Azure Speech service credentials
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION")

    # Initialize speech configuration
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Set audio output configuration to save to a WAV file
    file_name = "output.wav"
    audio_config = speechsdk.audio.AudioOutputConfig(filename=file_name)

    # Create a synthesizer with the audio output configuration
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Text to synthesize
    text = "Testing Azure Speech Service on Heroku."

    # Perform speech synthesis
    print("Starting speech synthesis...")
    result = synthesizer.speak_text_async(text).get()

    # Handle the result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech synthesized successfully. Audio saved to {file_name}")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")

if __name__ == "__main__":
    test_speech_synthesis()
