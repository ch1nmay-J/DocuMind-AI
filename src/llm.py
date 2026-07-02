import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


client = genai.Client(
    api_key = api_key
)


def generate_answer(question, context):

    prompt = f"""
You are a helpful assistant.

Answer ONLY using the context below.

If the answer is not present in the context, say:
'I couldn't find that information in the provided document.'

Context:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text