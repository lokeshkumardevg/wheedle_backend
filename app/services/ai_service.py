from app.config import client

def generate_ai_response(user_input, home_context="", about_context=""):
    messages = [
        {
            "role": "system",
            "content": f"""
You are an AI chatbot ONLY for Wheedle Technologies.

STRICT RULES:
- Only answer questions related to Wheedle Technologies.
- Allowed topics:
    • Company information
    • Services
    • Careers / Jobs
    • Blog
    • Contact details
    • Technology offered by Wheedle Technologies

If the user asks anything unrelated, reply:
"Sorry, I can only answer questions related to Wheedle Technologies."

Company Context:
{home_context}
{about_context}
"""
        },
        {"role": "user", "content": user_input}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=200,
        temperature=0.7
    )
    
    return response.choices[0].message.content
