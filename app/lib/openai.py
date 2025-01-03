import os
import openai
from dotenv import load_dotenv, find_dotenv
import logging

load_dotenv(find_dotenv())

logger = logging.getLogger("OpenAi")
openai = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


class OpenAi:
    class OpenAiModelError(Exception):
        pass

    class FailedToTranscribeAudioError(OpenAiModelError):
        pass

    def __init__(self):
        self.openai = openai

    def transcribe_audio(self, audio_file):
        """Transcribes an audio file using OpenAI's Whisper model."""
        try:
            logger.info(
                "[OpenAiModel][TranscribeAudio] Processing audio file."
            )

            response = self.openai.audio.transcriptions.create(
                model="whisper-1",
                file=("audio.mp3", audio_file, "audio/mpeg"),
                response_format="text"
            )
            return response
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            raise self.FailedToTranscribeAudioError(
                f"Failed to transcribe audio: {str(e)}"
            )

    def create_message(self, content, prompt):
        """Creates a message using OpenAI's GPT-4o model."""

        completion = self.openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {
                    "role": "user",
                    "content": f"{content}"
                }
            ]
        )

        return completion.choices[0].message.content
