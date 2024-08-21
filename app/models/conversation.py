from models.db import db
import logging


class ConversationModel(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)
    bot_name = db.Column(db.String)
    user_message = db.Column(db.String)
    agent_answer = db.Column(db.String)


class Conversation:
    logger = logging.getLogger("[ConversationModel]")

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

            cls.logger.info(
                f"[RegisterConversation] Finishing to register conversation: {conversation}"
            )
            cls.logger.info("[RegisterConversation] Finished registering conversation")

            return "Conversation registered"
        except Exception as exc:
            raise exc
