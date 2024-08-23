from app.config.utils import retrieve_prompt
from app.bots.openai_model import OpenAiModel

class Leo:
    """
    A RAG based bot that helps you to answer questions about Brazilian IRPF
    """
    def __init__(self):
        self.bot_name = "leo"
        self.head_prompt = retrieve_prompt(self.bot_name)
        self.openai_model = OpenAiModel(self.bot_name)
    
    def ask(self, user_message):
        return self.openai_model.generate_conversation(
            user_message=user_message,
            head_prompt=self.head_prompt,
            w_rag=True
        )