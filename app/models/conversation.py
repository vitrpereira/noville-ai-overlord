from app.models.db import db
from datetime import datetime
import logging
from sqlalchemy import create_engine, text
from dotenv import load_dotenv, find_dotenv
import os


load_dotenv(find_dotenv())


class ConversationModel(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)
    bot_name = db.Column(db.String)
    user_message = db.Column(db.String)
    agent_answer = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Conversation:
    logger = logging.getLogger("[ConversationModel]")
    postgres = os.environ.get('PRODUCTION_DATABASE_URI')

    @classmethod
    def register_conversation(
        cls, bot_name: str, user_message: str, agent_answer: str
    ) -> str:
        cls.logger.info("[RegisterConversation] Starting to register conversation")

        try:
            conversation = ConversationModel(
                bot_name=bot_name, user_message=user_message, agent_answer=agent_answer
            )

            db.session.add(conversation)
            db.session.commit()

            cls.logger.info("[RegisterConversation] Finished registering conversation")

            return "Conversation registered"
        except Exception as exc:
            raise exc

    
    @classmethod
    def leo_conversations(cls):
        sql = """
        SELECT *
        FROM conversations
        WHERE bot_name = 'leo'
        """.strip()

        return cls._sql_engine(sql)

    @classmethod
    def _sql_engine(cls, query):
        engine = create_engine(cls.postgres)

        with engine.connect() as con:
            rs = con.execute(text(query))
            cols = rs.keys()

            return [dict(zip(cols, row)) for row in rs.fetchall()]
