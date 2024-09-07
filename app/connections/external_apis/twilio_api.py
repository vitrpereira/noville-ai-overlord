from twilio.rest import Client
from app.connections.external_apis.external_api_client import ExternalApiClient
from dotenv import load_dotenv, find_dotenv
from typing import Optional
import os

load_dotenv(find_dotenv())


class TwilioApi(ExternalApiClient):

    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    @classmethod
    def post(
        cls,
        from_: str,
        to: str,
        bot_message: Optional[str] = None,
        media_url: Optional[str] = None
    ):
        payload = {
            'from_': 'whatsapp:' + from_,
            'to': 'whatsapp:' + to
        }

        if bot_message:
            payload['body'] = bot_message

        if media_url:
            payload['media_url'] = media_url

        message = cls.client.messages.create(**payload)
        return message.sid
