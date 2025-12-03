import os
import glob
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
from config.settings import settings
from services.document_processor import DocumentProcessor

class VectorStore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.index = None
    
    def load_or_create_index(self):
        if self.index is not None:
            return self.index
        
        if os.path.exists(settings.INDEX_PATH):
            self.index = FAISS.load_local(
                settings.INDEX_PATH, 
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
            return self.index
        
        processor = DocumentProcessor()
        documents = processor.load_documents()
        
        if not documents:
            raise ValueError("No documents found in data folder.")
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        all_chunks = splitter.split_documents(documents)
        
        self.index = FAISS.from_documents(all_chunks, self.embeddings)
        self.index.save_local(settings.INDEX_PATH)
        return self.index
    
    def similarity_search(self, query, k=4):
        index = self.load_or_create_index()
        return index.similarity_search(query, k=k)
    
    def reload_index(self):
        self.index = None
        if os.path.exists(settings.INDEX_PATH):
            os.remove(settings.INDEX_PATH)
        return self.load_or_create_index()