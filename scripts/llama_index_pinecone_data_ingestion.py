from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv, find_dotenv
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core import (
    download_loader,
    ServiceContext,
    VectorStoreIndex,
    StorageContext,
    SimpleDirectoryReader,
)
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.readers.file import PDFReader
import os

load_dotenv(find_dotenv())

DAFAULT_DOCS_DIR = "context_base"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 20

pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

if __name__ == "__main__":
    print("Pinecone started")
    parser = PDFReader()
    documents = SimpleDirectoryReader(
        input_dir=DAFAULT_DOCS_DIR, file_extractor={".pdf": parser}
    ).load_data()
    node_parser = SimpleNodeParser.from_defaults(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )

    llm = OpenAI(model="gpt-3.5-turbo", temperature=0)
    embed_model = OpenAIEmbedding(model="text-embedding-ada-002", embed_batch_size=100)
    service_context = ServiceContext.from_defaults(
        llm=llm, embed_model=embed_model, node_parser=node_parser
    )

    pc_index = pc.Index(os.environ["PINECONE_INDEX"])

    vector_store = PineconeVectorStore(pinecone_index=pc_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_documents(
        documents=documents,
        storage_context=storage_context,
        service_context=service_context,
        show_progress=True,
    )
