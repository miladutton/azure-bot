from question_data import questions
from speech.text_to_speech import speak_text

class CasualBot:
    """
    Bot logic for the Friendly and Casual version.
    Asks questions in a playful and engaging tone, with frequent pitch variation and humor.
    """
    def __init__(self):
        self.questions = iter(questions["friendly"])  # Load friendly bot questions
        self.current_question = None

    def get_next_question(self):
        """
        Retrieves the next question in the sequence.
        Returns None if no more questions are left.
        """
        try:
            self.current_question = next(self.questions)
            return self.current_question
        except StopIteration:
            return None

    def handle_error(self):
        """
        Error handling for unclear user input.
        Reassures the user with humor and a playful tone.
        """
        return "Oops! I didn’t catch that. Mind saying it again? No worries, take your time!"
