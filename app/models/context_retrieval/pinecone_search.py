import os
from dotenv import load_dotenv, find_dotenv
from pinecone import Pinecone
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import VectorStoreIndex


class PineconeSearch:
    def __init__(self):
        self.pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
        self.pc_index = self.pc.Index(os.environ["PINECONE_INDEX"])
        self.vector_store = PineconeVectorStore(pinecone_index=self.pc_index)

    def query_engine(self, user_input):
        query_eng = self.get_index().as_query_engine()
        return query_eng.query(user_input)

    def chat_engine(self):
        return self.get_index().as_chat_engine(chat_mode="context", verbose=True)

    def get_index(self) -> VectorStoreIndex:
        return VectorStoreIndex.from_vector_store(vector_store=self.vector_store)
