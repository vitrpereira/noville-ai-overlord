from flask import request, jsonify
import os
from dotenv import load_dotenv, find_dotenv
import yaml

load_dotenv(find_dotenv())


def require_api_key(func):
    def decorator(*args, **kwargs):
        api_key = request.headers.get("x-api-key")
        if not api_key or api_key != os.environ.get(
            "NOVILLE_AI_OVERLORD_API_KEY"
        ):
            response = jsonify({"message": "Invalid or missing API key"}), 401
            return response
        return func(*args, **kwargs)

    decorator.__name__ = func.__name__
    return decorator

def retrieve_prompt(bot_name):
    with open("bots_config.yml") as config:
        try:
            content = yaml.safe_load(config)
            return content['bots'][bot_name]['head_prompt'][0]
        except yaml.YAMLError as exc:
            raise Exception(f"An exception occurred while loading config files: {exc}")