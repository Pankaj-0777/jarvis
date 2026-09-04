import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5050))
    DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't')
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    VOICE_ENABLED = os.getenv('VOICE_ENABLED', 'True').lower() in ('true', '1', 't')
    DEFAULT_CITY = os.getenv('DEFAULT_CITY', 'London')
