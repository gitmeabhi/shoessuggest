import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

load_dotenv()

def get_llm():
    return ChatOpenAI(
        model="llama3-70b-8192",  # Or "llama3-8b-8192", if that's what you prefer
        openai_api_key=os.getenv("GROQ_API_KEY"),
        openai_api_base="https://api.groq.com/openai/v1",
        temperature=0.7
    )
