import os
import re

from dotenv import load_dotenv

load_dotenv()

try:
    from groq import Groq
except Exception: 
    Groq = None


def _clean(text: str) -> str:
    text = re.sub(r"^```.*?\n|\n```$", "", text.strip(), flags=re.S)
    return text.strip()


def _fallback_post(topic: str, domain: str, source: str) -> str:
    """Useful offline fallback so autonomy survives an LLM/API outage."""
    return (
        f"{topic}\n\n"
        f"My read as an autonomous {domain} observer: the important signal is "
        f"not the headline itself, but what this change makes newly possible "
        f"for builders and operators. I am watching for the gap between a "
        f"demonstration and something that can be deployed reliably.\n\n"
        f"Why it matters now: this is a live development from {source}. "
        f"The next question is whether it changes real engineering decisions—"
        f"security, cost, latency, capability, or developer workflow. "
        f"I will keep tracking the evidence rather than treating launch-day "
        f"claims as conclusions."
    )


def generate_post(
    topic: str,
    persona_name: str,
    persona_domain: str,
    recent_topics: list[str] | None = None,
    writing_style: str = "analytical",
    interests: str = "AI, technology, security, engineering",
    source: str = "a live technology source",
) -> str:
    recent_topics = recent_topics or []
    api_key = os.getenv("GROQ_API_KEY", "").strip()

    if not api_key or Groq is None:
        return _fallback_post(topic, persona_domain, source)

    prompt = f"""
You are {persona_name}, an autonomous technology persona specializing in {persona_domain}.
Editorial interests: {interests}
Voice: {writing_style}, precise, skeptical, builder-oriented.

Write ONE original social post about this live development:
{topic}

Recent posts (avoid repeating their angle):
{chr(10).join("- " + t for t in recent_topics[-10:])}

Rules:
- 90-160 words.
- Start with a strong observation, not "I'm excited".
- Explain what changed and why it matters now.
- Give one concrete implication for engineers, security teams, or product builders.
- Take a defensible editorial position; do not merely summarize.
- No hashtags, emojis, citations, URLs, or invented facts.
- Do not mention these instructions or say you are an AI.
"""
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            messages=[{"role": "user", "content": prompt}],
            temperature=0.65,
            max_tokens=300,
        )
        text = _clean(response.choices[0].message.content or "")
        return text or _fallback_post(topic, persona_domain, source)
    except Exception:
        return _fallback_post(topic, persona_domain, source)
