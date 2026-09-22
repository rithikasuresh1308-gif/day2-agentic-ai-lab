import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "groq")

if PROVIDER == "groq":
    BASE_URL = "https://api.groq.com/openai/v1"
    API_KEY = os.getenv("GROQ_API_KEY")
    MODEL = os.getenv("MODEL", "qwen/qwen3.8-27b")

    client = OpenAI(
        base_url=BASE_URL,
        api_key=API_KEY
    )

COURSE_FEES = {
    "CS101": 12000,
    "AI202": 18000,
    "DS303": 15000
}

QUESTIONS = [
    "What is the fee for AI202?",
    "What is the total fee for CS101 and AI202 after a 10% scholarship?",
    "Is DS303 more expensive than CS101, and by how much?",
    "Write a two-line welcome message for new AI students."
]