#!/usr/bin/env python3
"""
Main entry point for Steve Jobs AI Advisor
"""
import os
from interface.gradio_app import GradioApp
from config.settings import settings

def initialize_data_folder():
    os.makedirs(settings.DATA_DIR, exist_ok=True)
    
    sample_file = os.path.join(settings.DATA_DIR, "steve_jobs_quotes.txt")
    if not os.path.exists(sample_file):
        with open(sample_file, "w", encoding="utf-8") as f:
            f.write("""
"Stay hungry, stay foolish." - Steve Jobs

"Design is not just what it looks like. Design is how it works."

"Simple can be harder than complex. You have to work hard to get your thinking clean to make it simple."

"Your work is going to fill a large part of your life. The only way to be truly satisfied is to do what you believe is great work."

"Don't let the noise of others' opinions drown out your own inner voice."

"Have the courage to follow your heart and intuition."

"Great things in business are never done by one person. They're done by a team of people."

"Quality is more important than quantity. One home run is much better than two doubles."

"Sometimes when you innovate, you make mistakes. It is best to admit them quickly, and get on with improving your other innovations."
            """)

def main():
    print("Initializing Steve Jobs AI Advisor...")
    
    if not settings.OPENAI_API_KEY:
        print("Warning: OPENAI_API_KEY not found in environment variables.")
        print("Please set it in .env file or environment variables.")
    
    initialize_data_folder()
    
    print("Loading knowledge base...")
    from core.vector_store import VectorStore
    vector_store = VectorStore()
    vector_store.load_or_create_index()
    
    print("Launching Gradio interface...")
    app = GradioApp()
    interface = app.create_interface()
    interface.launch(
        server_name=settings.GRADIO_HOST,
        server_port=settings.GRADIO_PORT,
        debug=True
    )

if __name__ == "__main__":
    main()