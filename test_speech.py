import azure.cognitiveservices.speech as speechsdk

# Replace with your Azure Speech key and region
speech_key = "2ojPWe0ZTWbLxeV2mT5IxdwOyBtbcqEtlRZ7KQAkEY0aw3KeogqqJQQJ99ALACYeBjFXJ3w3AAAYACOG2s8I"
region = "eastus"

try:
    # Configure Azure Speech SDK
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Synthesize speech
    print("Testing Azure Speech SDK...")
    result = synthesizer.speak_text_async("Hello! This is a test of the Azure Speech Service.").get()

    # Handle results
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesis succeeded.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        print("Speech synthesis canceled. Reason:", cancellation.reason)
        print("Error details:", cancellation.error_details)
except Exception as e:
    print("An error occurred:", str(e))
