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
        self.base_audio_dir = "app/models/audio_files/"

    def generate_conversation(self, user_message, head_prompt=None):
        system_prompt = head_prompt if head_prompt else self.head_prompt

        try:
            assistant_answer = self.build_answer(system_prompt, user_message)
            logger.info(f"ASSISTANT_ANSWER: {assistant_answer}")
            return assistant_answer
        except Exception as e:
            raise e

    def build_answer(self, prompt, user_message):
        context = self.retrieve_context(user_message)
        system_prompt = f"[HEAD PROMPT]: {prompt} + [CONTEXT]: {context}"

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

    def transcription_client(self, file) -> str:
        audio_file = open(file, "rb")
        transcript = openai.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            response_format="verbose_json",
            timestamp_granularities=["word"],
        )

        return transcript.text

    def text_to_speech_client(self, text_file, filename="speech.mp3") -> None:
        output_dir = self.base_audio_dir + filename
        response = openai.audio.speech.create(
            model="tts-1", voice="alloy", input=text_file
        )
        return response.stream_to_file(output_dir)

    def translation_client(self, audio_file) -> str:
        logging.info(
            f"[OPENAI][AUDIO CLIENT] - Starting translation from {audio_file}"
        )
        audio_file = open(audio_file, "rb")
        translation = openai.audio.translations.create(
            model="whisper-1", file=audio_file
        )

        return translation.text
