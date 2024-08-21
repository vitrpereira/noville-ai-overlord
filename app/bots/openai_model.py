import os
import openai
from dotenv import load_dotenv, find_dotenv
import logging
from bots.context_retrieval.pinecone_search import PineconeSearch
from models.conversation import Conversation
from config.utils import retrieve_prompt, openai_model_version

load_dotenv(find_dotenv())

openai = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
logger = logging.getLogger("OpenAiModel")


class OpenAiModel:
    def __init__(self, bot_name):
        self.model = openai_model_version()
        self.bot_name = bot_name
        self.head_prompt = retrieve_prompt("generic")
        self.pinecone_search = PineconeSearch()

    def generate_conversation(self, user_message, head_prompt=None):
        system_prompt = head_prompt if head_prompt else ""

        try:
            assistant_answer = (
                openai.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_string(system_prompt, user_message),
                )
                .choices[0]
                .message.content
            )
            logger.info(f"ASSISTANT_ANSWER: {assistant_answer}")

            logger.info(f"Starting to commit conversation")

            Conversation.register_conversation(
                bot_name=self.bot_name,
                agent_answer=assistant_answer,
                user_message=user_message,
            )
            return assistant_answer
        except Exception as e:
            raise e

    @staticmethod
    def conversation_string(system_prompt, user_message):
        return [
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"{user_message}"},
        ]
