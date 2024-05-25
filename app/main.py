from flask import Flask, jsonify
from flask_smorest import Api
from dotenv import load_dotenv
import os
from db import db
from routes import bp

app = Flask(__name__)

app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)