# Flask
from flask import Flask
from flask_migrate import Migrate

# Tools
import logging
import os
from dotenv import load_dotenv, find_dotenv

# From app
from app.config.config import config
from app.routes import bp
from app.models.db import db


def create_app():
    app = Flask(__name__)
    load_dotenv(find_dotenv())

    app.config["API_TITLE"] = "noville-ai-overlord"
    app.config["API_VERSION"] = "V1"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config.from_object(config[os.environ.get("FLASK_ENV", "development")])
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


if __name__ == "__main__":
    create_app().run(debug=True)
