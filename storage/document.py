from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
import os
from config import CHUNK_SIZE

class DocumentManager:

    def __init__(self, openai_api_key):
        self.documents = {}
        self.database = None
        self.openai_api_key = openai_api_key

    def add_document(self, name, content):
        self.documents[name] = content

    def remove_document(self, name):
        if name in self.documents:
            del self.documents[name]

    def list_documents(self):
        return list(self.documents.keys())

    def create_embeddings_and_database(self, chunk_size=CHUNK_SIZE, chunk_overlap=0, separator=" "):
        text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap, separator=separator)
        all_docs = []
        for doc_content in self.documents.values():
            docs = text_splitter.split_documents(doc_content)
            all_docs.extend(docs)
        embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
        self.database = FAISS.from_documents(all_docs, embeddings)
