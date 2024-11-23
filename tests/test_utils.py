import pytest
import yaml
from unittest.mock import patch, mock_open
from flask import Flask
from app.config.utils import (
    require_api_key,
    retrieve_prompt,
    openai_model_version,
    validate_json_schema,
    retrieve_json_schema,
)


# Setup Flask app for testing
@pytest.fixture
def app():
    app = Flask(__name__)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


# Test require_api_key decorator
def test_require_api_key_valid(app, client):
    @app.route('/test')
    @require_api_key
    def protected_route():
        return {'status': 'success'}, 200

    with patch.dict('os.environ', {'NOVILLE_AI_OVERLORD_API_KEY': 'test-key'}):
        response = client.get('/test', headers={'x-api-key': 'test-key'})
        assert response.status_code == 200


def test_require_api_key_invalid(app, client):
    @app.route('/test')
    @require_api_key
    def protected_route():
        return {'status': 'success'}, 200

    with patch.dict('os.environ', {'NOVILLE_AI_OVERLORD_API_KEY': 'test-key'}):
        response = client.get('/test', headers={'x-api-key': 'wrong-key'})
        assert response.status_code == 401
        assert response.json == {'message': 'Invalid or missing API key'}


def test_require_api_key_missing(app, client):
    @app.route('/test')
    @require_api_key
    def protected_route():
        return {'status': 'success'}, 200

    response = client.get('/test')
    assert response.status_code == 401
    assert response.json == {'message': 'Invalid or missing API key'}


# Test retrieve_prompt
def test_retrieve_prompt_success():
    mock_yaml_content = '''
    bots:
        prompts:
            test_bot:
                head_prompt:
                    - "Test prompt"
    '''
    with patch('builtins.open', mock_open(read_data=mock_yaml_content)):
        result = retrieve_prompt('test_bot')
        assert result == 'Test prompt'


def test_retrieve_prompt_yaml_error():
    with patch('builtins.open', mock_open(read_data='invalid: yaml: content')):
        with patch('yaml.safe_load', side_effect=yaml.YAMLError('Test error')):
            with pytest.raises(Exception) as exc_info:
                retrieve_prompt('test_bot')
            assert 'An exception occurred while loading config files' in str(
                exc_info.value
            )


# Test openai_model_version
def test_openai_model_version_success():
    mock_yaml_content = '''
    bots:
        openai_model:
            model_version:
                - "gpt-4"
    '''
    with patch('builtins.open', mock_open(read_data=mock_yaml_content)):
        result = openai_model_version()
        assert result == 'gpt-4'


def test_openai_model_version_yaml_error():
    with patch('builtins.open', mock_open(read_data='invalid: yaml: content')):
        with patch('yaml.safe_load', side_effect=yaml.YAMLError('Test error')):
            with pytest.raises(Exception) as exc_info:
                openai_model_version()
            assert 'An exception occurred while loading config files' in str(
                exc_info.value
            )


# Test validate_json_schema decorator
def test_validate_json_schema_valid(app, client):
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"}
        },
        "required": ["name"]
    }

    @app.route('/test', methods=['POST'])
    @validate_json_schema(schema)
    def test_route():
        return {'status': 'success'}, 200

    response = client.post('/test', json={'name': 'test'})
    assert response.status_code == 200


def test_validate_json_schema_invalid(app, client):
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"}
        },
        "required": ["name"]
    }

    @app.route('/test', methods=['POST'])
    @validate_json_schema(schema)
    def test_route():
        return {'status': 'success'}, 200

    response = client.post('/test', json={'name': 123})  # Invalid type
    assert response.status_code == 400
    assert 'error' in response.json


# Test retrieve_json_schema
def test_retrieve_json_schema():
    mock_schema = '{"type": "object"}'
    with patch('builtins.open', mock_open(read_data=mock_schema)):
        result = retrieve_json_schema('test_schema')
        assert result == {"type": "object"}
