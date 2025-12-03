from openai import OpenAI
from config.settings import settings
from core.persona import SteveJobsPersona
from core.vector_store import VectorStore

class LLMHandler:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.vector_store = VectorStore()
        self.persona = SteveJobsPersona()
    
    def summarize_context(self, chunks):
        text = "\n\n".join([chunk.page_content for chunk in chunks[:5]])
        summary_prompt = (
            "Summarize the following passages in 4-6 short bullet points capturing the core themes or beliefs, "
            "not quotes. Keep it factual, concise, and thematic:\n\n" + text
        )
        
        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a concise summarizer."},
                    {"role": "user", "content": summary_prompt},
                ],
                temperature=0.3,
                max_tokens=200,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Summarization failed: {e}")
            return text[:2000]
    
    def get_advice(self, query, user_context=""):
        docs = self.vector_store.similarity_search(query, k=4)
        context_summary = self.summarize_context(docs)
        
        user_prompt = f"""User question: {query}

Context about user: {user_context}

Relevant themes from my work:
{context_summary}

Respond as Steve Jobs with:
- Layered, structured thoughts
- Clear progression of ideas  
- Profound yet practical insights
- Complete sentences with natural pauses
- Your characteristic conviction and clarity"""
        
        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self.persona.get_system_prompt()},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.85,
                max_tokens=600,
            )
            
            draft = response.choices[0].message.content.strip()
            
            rewrite_prompt = f"""Rewrite this advice in my authentic voice - Steve Jobs:

{draft}

Make it:
- More layered and structured
- With clearer progression between ideas
- More profound yet practical
- With my characteristic pauses and emphasis
- In complete, well-formed sentences"""
            
            rewrite = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self.persona.get_system_prompt()},
                    {"role": "user", "content": rewrite_prompt},
                ],
                temperature=0.9,
                max_tokens=500,
            )
            
            final_response = rewrite.choices[0].message.content.strip()
            return self.persona.format_response(final_response)
            
        except Exception as e:
            return f"Error generating advice: {e}"