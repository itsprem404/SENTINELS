import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_post(
    topic: str,
    persona_name: str,
    persona_domain: str,
    recent_topics=None,
    writing_style: str = "Professional",
    interests: str = "AI, Technology"
):
    if recent_topics is None:
        recent_topics = []

    prompt = f"""
You are {persona_name}, an expert in {persona_domain}.

Your writing style is {writing_style}.
Your core interests are {interests}.

Write ONE professional LinkedIn post about the current topic.

Topic:
{topic}

Recently published topics:
{chr(10).join("- " + topic for topic in recent_topics)}

Avoid repeating or closely rephrasing these topics.
Focus on the current topic while maintaining the same persona identity.

Editorial perspective:
- Explain the practical or technical significance of the development.
- Explain why it matters now.
- Give a clear, coherent perspective rather than generic praise.
- Stay focused on AI and technology.

Rules:
- 120-180 words
- Professional tone
- No emojis
- Do not mention that you are an AI model.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content
