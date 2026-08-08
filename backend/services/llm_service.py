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
    recent_topics=None
):

    if recent_topics is None:
        recent_topics = []

    prompt = f"""
You are {persona_name}, an expert in {persona_domain}.

Write ONE professional LinkedIn post.

Topic:
{topic}

Recently published topics:
{chr(10).join("- " + topic for topic in recent_topics)}

Avoid repeating or closely rephrasing these topics.
Focus on the current topic.

Rules:
- 120-180 words
- Professional tone
- No emojis
- Mention why this topic matters.
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