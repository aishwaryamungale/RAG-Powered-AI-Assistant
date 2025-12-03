import gradio as gr
import time
from config.settings import settings
from core.llm_handler import LLMHandler
from core.vector_store import VectorStore
from services.tts_service import TTSService
from services.feedback_service import FeedbackService

class GradioApp:
    def __init__(self):
        self.llm_handler = LLMHandler()
        self.tts_service = TTSService()
        self.feedback_service = FeedbackService()
        self.vector_store = VectorStore()
    
    def get_advice(self, query, user_context, include_audio=True):
        if not query:
            return "Please enter a question.", None
        
        result = self.llm_handler.get_advice(query, user_context)
        
        audio_file = None
        if include_audio and result and not result.startswith("Error"):
            audio_file = self.tts_service.generate_speech(result)
        
        return result, audio_file
    
    def reload_index(self):
        try:
            self.vector_store.reload_index()
            return "Knowledge base reloaded successfully!"
        except Exception as e:
            return f"Error: {e}"
    
    def get_system_status(self):
        try:
            index = self.vector_store.load_or_create_index()
            doc_count = getattr(index.index, "ntotal", "unknown")
            return f"System healthy -- {doc_count} documents indexed."
        except Exception as e:
            return f"Error: {e}"
    
    def create_interface(self):
        with gr.Blocks(title="Steve Jobs AI Advisor", theme=gr.themes.Soft()) as interface:
            gr.Markdown("""
            # Get Advice from Steve Jobs
            *Stay hungry, stay foolish.*
            
            Experience Steve's characteristic layered thinking and profound insights.
            """)
            
            with gr.Row():
                with gr.Column(scale=2):
                    query = gr.Textbox(
                        label="Your Question", 
                        lines=3, 
                        placeholder="What do you want advice on? Ask about innovation, design, life..."
                    )
                    context = gr.Textbox(
                        label="Additional Context (optional)", 
                        lines=2,
                        placeholder="Tell me more about your situation..."
                    )
                    with gr.Row():
                        ask = gr.Button("Get Advice", variant="primary", size="lg")
                        audio_toggle = gr.Checkbox(label="Include Steve's Voice", value=True)
                    
                    with gr.Accordion("System Controls", open=False):
                        with gr.Row():
                            reload_btn = gr.Button("Reload Knowledge Base")
                            status_btn = gr.Button("Check System Status")
                        sys_output = gr.Textbox(label="Status", interactive=False)
                        
                with gr.Column(scale=3):
                    advice_box = gr.Textbox(
                        label="Steve's Advice", 
                        lines=12, 
                        show_copy_button=True,
                        placeholder="Steve's layered wisdom will appear here..."
                    )
                    audio_output = gr.Audio(
                        label="Listen to Steve", 
                        type="filepath", 
                        visible=True
                    )
                    
                    with gr.Row():
                        feedback_type = gr.Radio(
                            ["Helpful", "Not Helpful", "Interesting"], 
                            label="Feedback", 
                            value="Helpful"
                        )
                        rating = gr.Slider(1, 5, label="Rating", value=5, step=1)
                    with gr.Row():
                        feedback_btn = gr.Button("Save Feedback")
                        feedback_output = gr.Textbox(label="Feedback Status", interactive=False)
            
            ask.click(
                fn=self.get_advice, 
                inputs=[query, context, audio_toggle], 
                outputs=[advice_box, audio_output]
            )
            
            reload_btn.click(
                fn=self.reload_index, 
                inputs=[], 
                outputs=sys_output
            )
            
            status_btn.click(
                fn=self.get_system_status, 
                inputs=[], 
                outputs=sys_output
            )
            
            feedback_btn.click(
                fn=lambda q, a, f, r: self.feedback_service.save_feedback(q, a, f, r), 
                inputs=[query, advice_box, feedback_type, rating], 
                outputs=feedback_output
            )
            
            return interface