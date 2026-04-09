from .pdf_service import load_pdf_content
from app.config import client

pdf_content = load_pdf_content("./Wheedle Technologies pdf.pdf")

def generate_ai_response(user_input):

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": f"""
You are the official AI assistant of Wheedle Technologies.

Rules:
- Provide detailed, comprehensive answers about Wheedle Technologies and its services based on the provided company information.
- If a user asks about services like "digital marketing", web development, or AI, explain how Wheedle Technologies provides these services in detail.
- Ensure the response is well-structured and highly relevant.
- ALWAYS append the following reference URL at the end of your response: https://wheedletechnologies.ai/

Company Information:
{pdf_content[:10000]}
"""
            },
            {"role": "user", "content": user_input}
        ],
        temperature=0.4,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()
