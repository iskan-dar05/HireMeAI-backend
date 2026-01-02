from groq import Groq
from app.core.config import settings


client = Groq(api_key=settings.GROQ_API_KEY)


model = "llama-3.3-70b-versatile"

