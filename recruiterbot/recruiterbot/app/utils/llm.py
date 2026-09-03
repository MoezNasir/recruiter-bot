import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


def get_llm(temperature: float = 0.3):
    return ChatGroq(
        api_key=os.environ["GROQ_API_KEY"],
        model="openai/gpt-oss-120b",
        temperature=temperature,
    )