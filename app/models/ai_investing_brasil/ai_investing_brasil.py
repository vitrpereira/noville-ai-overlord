from models.openai_model import OpenAiModel
from models.head_prompt import AI_INVESTING_BRAZIL_HEAD_PROMPT
from connections.external_apis.noville_api import NovilleApi
from models.context_retrieval.pinecone_search import PineconeSearch
import logging
import asyncio

logger = logging.getLogger("AI-INVESTING-BR-MODULE")


class AiInvestingBrasil:
    def __init__(self):
        self.openai_model = OpenAiModel()
        self.noville_api = NovilleApi()
        self.head_prompt = AI_INVESTING_BRAZIL_HEAD_PROMPT

    def post_tweet(self, user_message):
        try:
            assistant_answer = self.openai_model.generate_conversation(user_message)
            try:
                logger.info("Trying to send tweet...")
                self.noville_api.post_tweet(assistant_answer)
                logger.info("Tweet sent")
                return "Tweet sent!"
            except Exception as e:
                raise e
        except Exception as e:
            raise e
