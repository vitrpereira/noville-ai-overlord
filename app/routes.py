from flask import Blueprint, jsonify, request
from models.openai_model import OpenAiModel
from models.ai_investing_brasil.ai_investing_brasil import AiInvestingBrasil
from config.utils import require_api_key
import logging
import asyncio

logger = logging.getLogger("app_log")
bp = Blueprint("routes", __name__)


@bp.route("/overlord/generate_conversation", methods=["POST"])
@require_api_key
def generate_conversation():
    data = request.json
    param = data["message"]

    if not param or "message" not in data:
        return jsonify({"message": "You must input a message!"}), 400
    conversation = OpenAiModel().generate_conversation(param)
    return jsonify({"output": f"{conversation}"})


@bp.route("/overlord/send_tweet_ai", methods=["POST"])
@require_api_key
def send_tweet_ai():
    data = request.json
    tweet = data["tweet"]
    print(tweet)

    tweet_request = AiInvestingBrasil().post_tweet(tweet)
    return jsonify({"message": f"{tweet_request}"})
