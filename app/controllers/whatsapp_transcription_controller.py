from flask import request, Blueprint
from flask.views import MethodView
import requests
import logging
from dotenv import load_dotenv, find_dotenv
from app.lib.openai import OpenAi
import os
from app.lib.audio_processor import AudioProcessor
from app.models.user import User
from app.models.product import Product
from functools import cached_property

load_dotenv(find_dotenv())
logger = logging.getLogger("WhatsappTranscriptionController")
blp = Blueprint("WhatsappTranscriptionController", __name__)
log_prefix = "[WhatsappTranscriptionController]"


class WhatsappTranscriptionController(MethodView):
    def __init__(self):
        self.open_ai = OpenAi()
        self.access_token = os.environ.get("WHATSAPP_ACCESS_TOKEN")
        self.product_name = 'whatsapp_transcription'

    def get(self):
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if verify_token == os.environ.get('WHATSAPP_PING_TOKEN'):
            return challenge, 200
        else:
            return "Unauthorized", 401

    def post(self):
        data = request.json
        logger.info(f"Received webhook data: {data}")

        if self._is_event_status_webhook(data): 
            return '', 200

        try:
            phone_number = self._get_phone(data)

            if self._first_interaction(data, phone_number):
                return '', 200

            if self._is_audio_message(data):
                message = self._process_audio_message(data)
            elif self._is_text_message(data):
                message = self._process_text_message(data)
            else:
                logger.error(f"Unhandled event type: {data}")
                message = "Ops! Não podemos processar ainda este tipo de conteúdo."
                message += " Mas não se preocupe, já estamos trabalhando para isso!"
                message += "\n\nPor hora, você pode enviar ou encaminhar um áudio, e a gente transforma em texto pra você! 😊"

            self.send_whatsapp_text_message(
                phone_number,
                message
            )
            return '', 200
        except Exception as e:
            logger.error(f"Error: {e}")
            self.send_whatsapp_text_message(
                phone_number,
                self._failed_message()
            )

            return '', 200
        
    def send_whatsapp_text_message(self, phone_number, text=''):
        phone_number_id = os.environ.get('WHATSAPP_PHONE_NUMBER_ID')

        logger.info(f'SENDER PHONE NUMBER: {phone_number}')

        body={
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            "text": {"body": text}
        }

        self.send_whatsapp_message(body, phone_number_id)
        return ""

    def send_whatsapp_message(self, body, phone_number_id):
        headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
        response = requests.post(
            f"https://graph.facebook.com/v16.0/{phone_number_id}/messages", 
            json=body, 
            headers=headers
        )

        if response.status_code == 200:
            logger.info(f"[SendWhatsappMessage] Message sent successfully")
        else:
            logger.error(f"[SendWhatsappMessage] Failed to send message: {response.status_code} - {response.text}")

        return ""

    def _first_interaction(self, data, phone_number: str):

        if User.exists_user_by_phone_number_and_product_id(
            phone_number, 
            self._product_id
        ):
            logger.info(
                f"User with phone number: '{phone_number}' already registered for '{self.product_name}' product"
            )
            return False

        user_name = self._get_user_name(data)

        User.register_user(
            phone_number,
            user_name,
            self._product_id
        )

        self.send_welcome_message(phone_number, user_name)
        # Send audio message if user sends one in the first interaction
        if self._is_audio_message(data):
            self.send_whatsapp_text_message(
                phone_number,
                self._process_audio_message(data)
            )

        return True
    
    def send_welcome_message(self, phone_number, user_name):
        welcome_message = f"Olá, *{user_name}*! Seja bem-vindo ao bot de transcrição de áudio para texto da Noville!"
        welcome_message += "\n\nPara utilizar o serviço, basta enviar ou encaminhar um áudio para este número."
        
        # Send welcome message
        self.send_whatsapp_text_message(
            phone_number,
            welcome_message
        )

        return ""
    
    @cached_property
    def _product_id(self):
        return Product.get_product_by_name(self.product_name).id

    def _process_audio_message(self, data):
        media_id = self._webhook_message_path(data)['audio']['id']
        audio_file = AudioProcessor.download_whatsapp_audio(media_id)
        
        if audio_file:
            try:
                transcription = self.open_ai.transcribe_audio(audio_file)
                message = "Aqui está a transcrição do seu áudio ✨:\n\n"
                message += transcription
            except OpenAi.FailedToTranscribeAudioError as e:
                logger.error(f"Error: {str(e)}")
                message = self._failed_message()
        else:
            message = self._failed_message()

        return message
    
    def _process_text_message(self, data):
        if self._is_message_webhook(data):
            if 'text' in self._webhook_message_path(data):
                message = "Ops! Parece que você enviou uma mensagem de texto. Por enquanto, podemos te ajudar somente com mensagens de *áudio*."
                message += "\n\nMas por curiosidade, sabia que sua mensagem em mandarim fica assim? ⛩️🧧🥢"
                message += "\n\n"

                message += self.open_ai.create_message(
                    self._webhook_message_path(data)['text']['body'],
                    "You are an mandarim translator. Translate this text to mandarim."
                )
                return message
            return ''
        return ''

    def _process_event_webhook(self, data):
        # Hold this logic for future database operations
        if self._is_event_status_webhook(data):
            if 'statuses' in (data_path := self._basic_data_path(data)):
                event = data_path['statuses'][0]['status']
                logger.info(f"[EventWebHook]: Message was '{event}'")

                return event
            return ''
        return ''

    def _is_event_status_webhook(self, data):
        if 'statuses' in self._basic_data_path(data):
            return True
        return False

    def _is_message_webhook(self, data):
        if 'messages' in self._basic_data_path(data): 
            return True
        return False

    def _is_audio_message(self, data):
        if self._is_message_webhook(data):
            if 'audio' in self._webhook_message_path(data):
                return True
        return False
    
    def _is_text_message(self, data):
        if self._is_message_webhook(data):
            if 'text' in self._webhook_message_path(data):
                return True
        return False

    def _get_phone(self, data):
        return self._basic_data_path(data)['contacts'][0]['wa_id']
    
    def _get_user_name(self, data):
        return self._basic_data_path(data)['contacts'][0]['profile']['name']

    def _basic_data_path(self, data):
        return data['entry'][0]['changes'][0]['value']
    
    def _webhook_message_path(self, data):
        return self._basic_data_path(data)['messages'][0]
    
    @staticmethod
    def _failed_message():
        failed_message = "Ops, nosso serviço está indisponível no momento e não conseguimos processar sua mensagem."
        failed_message += "\nPor favor, tente novamente em alguns instantes."

        return failed_message

blp.add_url_rule(
    '/overlord/whatsapp/transcription',
    view_func=WhatsappTranscriptionController.as_view('whatsapp_transcription_controller')
)
