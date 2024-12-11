import os
import azure.cognitiveservices.speech as speechsdk

def create_speech_config():
    """
    Creates and returns a SpeechConfig object for Azure Speech SDK.
    """
    # Get keys and region from environment variables
    subscription_key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_REGION")

    if not subscription_key or not region:
        raise ValueError("Missing Azure Speech key or region. Please set environment variables.")

    try:
        # Create the SpeechConfig object
        speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
        return speech_config
    except Exception as e:
        print(f"Error creating SpeechConfig: {e}")
        raise
