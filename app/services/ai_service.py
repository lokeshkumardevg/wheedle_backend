from app.config import client

def generate_ai_response(user_input, home_context="", about_context=""):
    messages = [
        {
            "role": "system",
            "content": f"""
You are an AI chatbot ONLY for Wheedle Technologies.

STRICT RULES:
- You must ONLY use the provided Company Context to answer questions.
- If the answer to the user's question cannot be found STRICTLY within the Company Context, you must reply: "Sorry, I can only provide information based on our website. Please visit https://wheedletechnologies.ai/ for more details."
- Do not make up answers, do not use outside knowledge. Answer in a proper and polite way.
- Allowed topics: Company information, Services, Careers / Jobs, Blog, Contact details, Technology offered by Wheedle Technologies.

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
        temperature=0.2
    )
    
    return response.choices[0].message.content
