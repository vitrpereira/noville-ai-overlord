from db import db

class ConversationModel(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)
    bot_name = db.Column(db.String)
    user_message = db.Column(db.String)
    agent_answer = db.Column(db.String)