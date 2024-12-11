import os
import azure.cognitiveservices.speech as speechsdk

def create_speech_config():
    """
    Creates and returns a SpeechConfig object for Azure Speech SDK using environment variables.
    Returns:
        - SpeechConfig object.
    """
    try:
        subscription_key = os.getenv("AZURE_SPEECH_KEY")
        region = os.getenv("AZURE_REGION")

        if not subscription_key or not region:
            raise ValueError("Missing Azure Speech key or region. Ensure they are set as environment variables.")

        speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
        return speech_config
    except Exception as e:
        print(f"Error creating SpeechConfig: {e}")
        raise


def recognize_speech():
    """
    Captures and processes speech input from the user's microphone.
    Returns:
        - Recognized text or an error message.
    """
    try:
        # Create speech and audio configurations
        speech_config = create_speech_config()
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        print("Listening... Speak into your microphone.")
        result = recognizer.recognize_once()

        # Handle different results
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return result.text
        elif result.reason == speechsdk.ResultReason.NoMatch:
            return "No speech could be recognized."
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech recognition canceled: {cancellation_details.reason}")
            if cancellation_details.error_details:
                print(f"Error details: {cancellation_details.error_details}")
            return None
    except Exception as e:
        print(f"Error recognizing speech: {e}")
        raise


# Example usage (can be removed or commented out in production)
if __name__ == "__main__":
    # Test the recognize_speech function
    recognized_text = recognize_speech()
    if recognized_text:
        print(f"Recognized Speech: {recognized_text}")
    else:
        print("Speech recognition failed.")
