from flask import request, jsonify
import os
from dotenv import load_dotenv, find_dotenv
import yaml
import jsonschema
from jsonschema import validate
import json
import logging


load_dotenv(find_dotenv())
bots_config_file = "app/config/bots_config.yml"
logger = logging.getLogger(__name__)


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
    with open(bots_config_file) as config:
        try:
            content = yaml.safe_load(config)
            return content["bots"]["prompts"][bot_name]["head_prompt"][0]
        except yaml.YAMLError as exc:
            raise Exception(
                f"An exception occurred while loading config files: {exc}"
            )


def openai_model_version():
    with open(bots_config_file) as config:
        try:
            content = yaml.safe_load(config)
            return content["bots"]["openai_model"]["model_version"][0]
        except yaml.YAMLError as exc:
            raise Exception(
                f"An exception occurred while loading config files: {exc}"
            )


def validate_json_schema(schema):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                request_json = request.json
                validate(request_json, schema)
                return func(*args, **kwargs)
            except jsonschema.exceptions.ValidationError as e:
                logger.error(f"Validation error: {e}")
                return jsonify({"error": str(e.message)}), 400

        return wrapper
    return decorator


def retrieve_json_schema(schema_name):
    base_path = 'app/config/api_schemas'
    with open(f"{base_path}/{schema_name}.json") as schema_file:
        return json.load(schema_file)
