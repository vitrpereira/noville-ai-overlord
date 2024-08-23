import os
import openai
from dotenv import load_dotenv, find_dotenv
import logging
from app.bots.context_retrieval.pinecone_search import PineconeSearch
from app.models.conversation import Conversation
from app.config.utils import retrieve_prompt, openai_model_version

load_dotenv(find_dotenv())

openai = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
logger = logging.getLogger("OpenAiModel")


class OpenAiModel:
    def __init__(self, bot_name: str):
        self.bot_name = bot_name.lower()
        self.model = openai_model_version()
        self.head_prompt = retrieve_prompt("generic")


    def generate_conversation(self, 
        user_message: str, head_prompt: str = None, w_rag: bool = False
    ) -> str:
        logger.debug(f"[USER MESSAGE] {user_message}")
        system_prompt = head_prompt if head_prompt else self.head_prompt
        system_prompt +=  self._pinecone_context(user_message) if w_rag else ''
        user_input = f"[USER MESSAGE] {user_message}"

        try:
            assistant_answer = (
                openai.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_string(system_prompt, user_input),
                )
                .choices[0]
                .message.content
            )

            logger.info(f"[GenerateConversation] {user_input}")
            logger.info(f"[GenerateConversation] ASSISTANT ANSWER: {assistant_answer}")

            Conversation.register_conversation(
                bot_name=self.bot_name,
                agent_answer=assistant_answer,
                user_message=user_message,
            )
            return assistant_answer
        except Exception as e:
            raise e
        
    def _pinecone_context(self, user_message):
        return "[CONTEXT]" + str(PineconeSearch.query_engine(user_message))

    @staticmethod
    def conversation_string(system_prompt, user_message):
        conversation = [
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"{user_message}"},
        ]

        return conversation
