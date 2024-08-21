from flask import Blueprint, jsonify, request
from bots.openai_model import OpenAiModel
from config.utils import require_api_key
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
