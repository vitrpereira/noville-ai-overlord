from flask import Blueprint, jsonify, request
from resources.openai_model import OpenAiModel
from config.utils import require_api_key


bp = Blueprint('routes', __name__)

@bp.route('/overlord/generate_conversation', methods=["POST"])
@require_api_key
def generate_conversation():
    data = request.json
    param = data['message']
    
    if not param or 'message' not in data:
        return jsonify({'message': 'You must input a message!'}), 400
    return OpenAiModel().generate_conversation(param)