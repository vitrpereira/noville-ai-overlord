import os 
import openai
from dotenv import load_dotenv, find_dotenv
import logging
import json

from connections.external_apis.noville_api import NovilleApi
from .head_prompt import HEAD_PROMPT

load_dotenv(find_dotenv())

openai = openai.OpenAI(api_key= os.environ.get('OPENAI_API_KEY'))
logger = logging.getLogger('open-ai-module-log')

class OpenAiModel:
    def __init__(self):
        self.model = "gpt-3.5-turbo"
        self.noville_api = NovilleApi()

    def generate_conversation(self, user_message):
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=self.conversation_string(user_message)
            )

            assistant_answer = response.choices[0].message.content
            logger.info(f"ASSISTANT_ANSWER: {assistant_answer}")
            try:
                self.noville_api.post_tweets(assistant_answer)
            except Exception as e:
                raise e
            return assistant_answer
        except Exception as e:
            raise e


    def conversation_string(self, user_message):
        return [
                    {
                        'role': 'system',
                        "content": f'{HEAD_PROMPT}'
                    }, 
                    {
                        'role': 'user',
                        'content': f'{user_message}'
                    }
                ]