import os
from dotenv import load_dotenv, find_dotenv
from pinecone import Pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import VectorStoreIndex
import logging


load_dotenv(find_dotenv())
logger = logging.getLogger("PineconeSearch")


class PineconeSearch:
    pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
    pc_index = pc.Index(os.environ["PINECONE_INDEX"])
    vector_store = PineconeVectorStore(pinecone_index=pc_index)

    @classmethod
    def query_engine(cls, user_message):
        query_eng = cls._get_index().as_query_engine()
        return query_eng.query(user_message)

    @classmethod
    def chat_engine(cls, user_message):
        response = cls._get_index().as_chat_engine(
            chat_mode="context", verbose=True
            ).chat(
                message=user_message
                )
        logger.info(f"[CHAT ENGINE] Response: {response}")
        return response

    @staticmethod
    def _get_index() -> VectorStoreIndex:
        return VectorStoreIndex.from_vector_store(
            vector_store=PineconeSearch.vector_store
            )
