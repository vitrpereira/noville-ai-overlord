from flask import request, jsonify
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def require_api_key(f):
    def decorator(*args, **kwargs):
        api_key = request.headers.get("x-api-key")
        if not api_key or api_key != os.environ.get(
            "NOVILLE_AI_OVERLORD_API_KEY"
        ):
            response = jsonify({"message": "Invalid or missing API key"}), 401
            return response
        return f(*args, **kwargs)

    decorator.__name__ = f.__name__
    return decorator
