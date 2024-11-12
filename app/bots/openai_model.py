import os
import openai
from dotenv import load_dotenv, find_dotenv
import logging
from app.bots.context_retrieval.pinecone_search import PineconeSearch
from app.models.conversation import Conversation
from app.config.utils import retrieve_prompt, openai_model_version

load_dotenv(find_dotenv())

logger = logging.getLogger("OpenAiModel")
openai = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class OpenAiModel:
    def __init__(self):
        self.openai = openai

        
    def transcribe_audio(self, audio_file):
        transcript = self.openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

        return transcript.text