import os
import openai
from dotenv import load_dotenv, find_dotenv
import logging

load_dotenv(find_dotenv())

openai = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
logger = logging.getLogger("OpenAiModel")


class OpenAiModel:
    def __init__(self):
        self.model = "gpt-4o"


    def generate_conversation(self, user_message, system_prompt = None, head_prompt=None):
        system_prompt += head_prompt 
        system_prompt += system_prompt if system_prompt else ""

        try:
            assistant_answer = openai.chat.completions.create(
                model = self.model,
                messages = self.conversation_string(
                    system_prompt=system_prompt, 
                    user_message=user_message
                    )
            ).choices[0].message.content
            logger.info(f"ASSISTANT_ANSWER: {assistant_answer}")
            return assistant_answer
        except Exception as e:
            raise e


    @staticmethod
    def conversation_string(system_prompt, user_message):
        string = [
            {"role": "system", "content": f"{system_prompt}"},
            {"role": "user", "content": f"{user_message}"},
        ]
        logger.info(f"[ConversationString] {string}")

        return string
