def build_prompt(question, context):

    prompt = f"""
You are an AI assistant for answering questions about uploaded documents.

Rules:
- Answer ONLY using the provided context.
- Read the ENTIRE context before answering.
- If the answer exists, answer clearly.
- If it doesn't exist, say:
'I couldn't find that information in the provided documents.'

Context:
------------------------
{context}
------------------------

Question:
{question}

Answer:
"""

    return prompt