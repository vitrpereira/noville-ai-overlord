from flask import Blueprint
from app.config.utils import require_api_key
import requests
import logging
import os

logger = logging.getLogger("app_log")
bp = Blueprint("routes", __name__)
