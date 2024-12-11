import azure.cognitiveservices.speech as speechsdk

def speak_text(config, text, style="neutral", pitch="0%", rate="0.9"):
    """
    Converts text to speech using Azure Speech SDK with the specified style, pitch, and rate.
    """
    ssml = f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
        <voice name="en-US-AriaNeural">
            <mstts:express-as style="{style}">
                <prosody pitch="{pitch}" rate="{rate}">
                    {text}
                </prosody>
            </mstts:express-as>
        </voice>
    </speak>
    """
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=config)
    synthesizer.speak_ssml_async(ssml).get()
