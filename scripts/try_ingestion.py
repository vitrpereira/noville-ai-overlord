from dotenv import load_dotenv, find_dotenv
import os
from pinecone import Pinecone, ServerlessSpec
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core.callbacks import LlamaDebugHandler, CallbackManager
from llama_index.core import ServiceContext, Settings
from langfuse.llama_index import LlamaIndexCallbackHandler

load_dotenv(find_dotenv())

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
langfuse_callback_handler = LlamaIndexCallbackHandler()
Settings.callback_manager = CallbackManager([langfuse_callback_handler])

if __name__ == "__main__":
    print("RAG...")

    pc_index = pc.Index(os.environ["PINECONE_INDEX"])
    vector_store = PineconeVectorStore(pinecone_index=pc_index)

    llama_debug = LlamaDebugHandler(print_trace_on_end=True)
    callback_manager = CallbackManager(handlers=[llama_debug])
    service_context = ServiceContext.from_defaults(callback_manager=callback_manager)

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store, service_context=service_context
    )

    query = "Wha are Warren Buffet's investment principles?"
    query_engine = index.as_query_engine()
    response = query_engine.query(query)

    langfuse_callback_handler.flush()

    print(response)
