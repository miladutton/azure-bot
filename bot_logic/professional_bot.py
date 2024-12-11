from question_data import questions
from speech.text_to_speech import speak_text

class ProfessionalBot:
    """
    Bot logic for the Professional version.
    Asks questions in a formal tone and processes responses.
    """
    def __init__(self):
        self.questions = iter(questions["professional"])  # Load professional bot questions
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
        Error handling for unclear user input, provides logical next steps.
        """
        return "I didn't understand your response. Please provide more details or clarify."
