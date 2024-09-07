from flask import Blueprint, jsonify, request
from app.bots.openai_model import OpenAiModel
from app.bots.leo.leo import Leo
from app.bots.veronica.veronica import Veronica
from app.config.utils import require_api_key
from app.connections.external_apis.twilio_api import TwilioApi
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


@bp.route("/overlord/veronica", methods=["POST"])
@require_api_key
def temp_text_to_audio():
    data = request.json
    param = data["message"]

    if not param or "message" not in data:
        return jsonify({"message": "You must input a message!"}), 400
    conversation = Veronica().call(param)
    return jsonify({"message": conversation})


@bp.route("/overlord/twilio_messager", methods=["POST"])
@require_api_key
def twilio_messager():
    data = request.json
    param = data["message"]

    if not param or "message" not in data:
        return jsonify({"message": "You must input a message!"}), 400
    conversation = TwilioApi.post(media_file=param)
    return jsonify({"message": conversation})


@bp.route("/overlord/test_leo", methods=["POST"])
@require_api_key
def test_leo():
    data = request.json
    param = data["message"]

    conversation = Leo().ask(param)
    return jsonify({"message": f"{conversation}"})
