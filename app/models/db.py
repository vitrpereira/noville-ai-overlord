from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, text
from dotenv import load_dotenv, find_dotenv
import os

db = SQLAlchemy()

load_dotenv(find_dotenv())


class Base:
    postgres = os.environ.get('PRODUCTION_DATABASE_URI')

    @classmethod
    def sql_engine(cls, query):
        engine = create_engine(cls.postgres)

        with engine.connect() as con:
            rs = con.execute(text(query))
            cols = rs.keys()

            return [dict(zip(cols, row)) for row in rs.fetchall()]