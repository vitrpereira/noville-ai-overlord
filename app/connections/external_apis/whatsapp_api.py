from app.connections.external_apis.external_api import ExternalApi
import os
from dotenv import load_dotenv, find_dotenv
import logging

logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

class WhatsappApi(ExternalApi):
    ACCESS_TOKEN = os.environ.get('WHATSAPP_ACCESS_TOKEN')
    BASE_URL = "https://graph.facebook.com/v16.0"

    @classmethod
    def send_message(cls, body, phone_number_id):
        response = cls.perform(
            endpoint_url=f"{cls.BASE_URL}/{phone_number_id}/messages", 
            verb="post",
            payload=body, 
            headers=cls._headers()
        )

        if response.status_code == 200:
            logger.info(
                f"[SendWhatsappMessage] Message sent successfully"
            )
            return ''
        else:
            logger.error(
                f"[SendWhatsappMessage] Failed to send message: {response.status_code} - {response.text}"
            )

    @staticmethod
    def _headers():
        return { "Authorization": f"Bearer {WhatsappApi.ACCESS_TOKEN}" }
