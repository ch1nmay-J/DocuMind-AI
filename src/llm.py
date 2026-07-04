from src.prompt_builder import build_prompt
from src.config import LLM_MODEL
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


client = genai.Client(
    api_key = api_key
)


def generate_answer(question, context):

    prompt = build_prompt(question, context)

    try:

        response = client.models.generate_content(
        model=LLM_MODEL,
        contents=prompt,
        )

        return response.text

    except Exception as e:

        return f"Error while generating response:\n{str(e)}"
