import os
import openai
from dotenv import load_dotenv, find_dotenv
import logging
from models.context_retrieval.pinecone_search import PineconeSearch
from models.head_prompt import BASIC_HEAD_PROMPT

load_dotenv(find_dotenv())

openai = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
logger = logging.getLogger("open-ai-module-log")


class OpenAiModel:
    def __init__(self):
        self.model = "gpt-3.5-turbo"
        self.head_prompt = BASIC_HEAD_PROMPT
        self.pinecone_search = PineconeSearch()

    def generate_conversation(self, user_message, head_prompt=None):
        system_prompt = self.head_prompt if head_prompt is None else head_prompt

        try:
            assistant_answer = self.retrieve_context(system_prompt, user_message)
            logger.info(f"ASSISTANT_ANSWER: {assistant_answer}")
            return assistant_answer
        except Exception as e:
            raise e

    def build_answer(self, prompt, user_message):
        context = self.retrieve_context(user_message)
        system_prompt = f"HEAD PROMPT: {prompt} + QUESTION CONTEXT: {context}"

        logger.info(f"PINECONE CONTEXT: {context}")

        return self.conversation_string(system_prompt, user_message)

    def retrieve_context(self, user_message):
        return self.pinecone_search.query_engine(user_message)

    @staticmethod
    def conversation_string(system_prompt, user_message):
        return [
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"{user_message}"},
        ]
