from question_data import questions
from speech.text_to_speech import speak_text

class ModerateBot:
    """
    Bot logic for the Moderate version.
    Asks questions in a warm and conversational tone, with light empathy.
    """
    def __init__(self):
        self.questions = iter(questions["moderate"])  # Load moderate bot questions
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
        Error handling for unclear user input, acknowledges the issue calmly and offers a practical solution.
        """
        return "I'm sorry, I didn’t catch that. Could you please clarify or share more details?"
