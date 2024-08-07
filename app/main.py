from flask import Flask
from routes import bp
import logging


def app():

    app = Flask(__name__)
    logger = logging.getLogger(__name__)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger.info("Application started")

    app.register_blueprint(bp)

    return app.run(debug=True)


if __name__ == "__main__":
    app()
