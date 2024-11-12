from flask import Blueprint, jsonify, request
from app.bots.openai_model import OpenAiModel
from app.bots.veronica.veronica import Veronica
from app.config.utils import require_api_key
import logging

logger = logging.getLogger("app_log")
bp = Blueprint("routes", __name__)


@bp.route("/overlord/generate_conversation", methods=["POST"])
@require_api_key
def generate_conversation():
    data = request.json
    param = data["message"]

    if not param or "message" not in data:
        return jsonify({"message": "You must input a message!"}), 400
    conversation = OpenAiModel("EndpointClient").generate_conversation(param)
    return jsonify({"message": f"{conversation}"})


@bp.route("/overlord/veronica/transcribe_audio", methods=["POST"])
@require_api_key
def temp_text_to_audio():
    data = request.json
    param = data["audio_path"]

    if not param or "audio_path" not in data:
        return jsonify({"error": "You must input a message!"}), 400
    return jsonify({"your_audio_text": OpenAiModel().transcribe_audio(param)})
