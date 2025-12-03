import re
from openai import OpenAI
from config.settings import settings

class TTSService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def generate_speech(self, text, voice=None):
        if voice is None:
            voice = settings.TTS_VOICE
        
        try:
            clean_text = re.sub(r'[*•\-]', '', text)
            clean_text = re.sub(r'\n+', '. ', clean_text)
            
            response = self.client.audio.speech.create(
                model=settings.TTS_MODEL,
                voice=voice,
                input=clean_text[:4096]
            )
            
            audio_file = "steve_response.mp3"
            response.stream_to_file(audio_file)
            return audio_file
        except Exception as e:
            print(f"TTS Error: {e}")
            return None