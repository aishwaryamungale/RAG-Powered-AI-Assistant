import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    Openai_key = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    
    DATA_DIR = "./data"
    INDEX_PATH = "steve_jobs_index.faiss"
    FEEDBACK_FILE = "steve_jobs_feedback.xlsx"
    
    CHUNK_SIZE = 800
    CHUNK_OVERLAP = 100
    
    TTS_VOICE = "onyx"
    TTS_MODEL = "tts-1"
    
    GRADIO_PORT = 7860
    GRADIO_HOST = "localhost"

settings = Settings()