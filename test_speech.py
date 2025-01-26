import azure.cognitiveservices.speech as speechsdk

def test_speech_synthesis():
    # Replace with your Azure Speech subscription key and region
    subscription_key = "YOUR_AZURE_SPEECH_KEY"
    region = "YOUR_AZURE_REGION"

    # Configure Azure Speech
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)

    # Log for debugging
    speech_config.set_property(speechsdk.PropertyId.Speech_LogLevel, "All")

    # Synthesize speech
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_text_async("Testing Azure Speech in Heroku").get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesis succeeded!")
    else:
        print(f"Speech synthesis failed. Reason: {result.reason}")

if __name__ == "__main__":
    test_speech_synthesis()
