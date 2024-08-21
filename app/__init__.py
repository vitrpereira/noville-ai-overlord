from flask import Flask
from app.routes import bp
import logging
import os
from dotenv import load_dotenv, find_dotenv
from app.models.db import db
from flask_migrate import Migrate

def app():
    app = Flask(__name__)
    load_dotenv(find_dotenv())

    app.config["API_TITLE"] = "noville-ai-overlord"
    app.config["API_VERSION"] = "V1"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    migrate = Migrate(app, db)

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger.info("Application started")

    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app
