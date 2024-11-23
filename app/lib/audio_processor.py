# flake8: noqa

import requests
import os
from dotenv import load_dotenv, find_dotenv
import logging
import io
from pydub import AudioSegment

load_dotenv(find_dotenv())

logger = logging.getLogger("AudioProcessor")
log_prefix = "[AudioProcessor]"


class AudioProcessor:
    ACCESS_TOKEN = os.environ.get('WHATSAPP_ACCESS_TOKEN')

    @classmethod
    def download_whatsapp_audio(cls, media_id):
        url = f"https://graph.facebook.com/v16.0/{media_id}"
        headers = {
            "Authorization": f"Bearer {cls.ACCESS_TOKEN}"
        }
    
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            logger.info(f"{log_prefix} Fetched audio content {response.json()}")

            audio_url = response.json().get("url")
            audio_response = requests.get(audio_url, headers=headers)
            
            if audio_response.status_code == 200:
                logger.info(f"{log_prefix} Successfully fetched audio response!")

                audio_file = io.BytesIO(audio_response.content)
                return cls.convert_audio_to_mp3(audio_file)
            else:
                logger.error(f"Failed to download audio file: {audio_response.status_code} - {audio_response.text}")
        else:
            logger.error(f"Failed to get audio URL: {response.status_code} - {response.text}")

        return None

    @classmethod
    def convert_audio_to_mp3(cls, audio_file):
        """Convert downloaded audio to MP3 and return as BytesIO."""
        try:
            audio = AudioSegment.from_file(audio_file, format="ogg")
            output_io = io.BytesIO()
            audio.export(output_io, format="mp3")
            output_io.seek(0) 
            logger.info(f"Audio successfully converted to MP3 in memory.")
            return output_io
        except Exception as e:
            logger.error(f"Error converting audio: {e}")
            return None
