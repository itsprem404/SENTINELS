import re
from typing import Any


TECH_KEYWORDS = {
    "ai", "artificial intelligence", "machine learning", "llm", "model",
    "generative ai", "agent", "agents", "inference", "reasoning", "openai",
    "anthropic", "google", "deepmind", "gemini", "claude", "gpt", "hugging face",
    "huggingface", "mistral", "meta ai", "robotics", "python", "developer",
    "programming", "software", "github", "open source", "cybersecurity",
    "security", "vulnerability", "malware", "cloud", "semiconductor", "gpu",
    "chip", "datacenter", "developer tools", "api", "computer vision",
    "natural language", "rl", "reinforcement learning", "robot", "automation",
}

REJECT_KEYWORDS = {
    "football", "cricket", "movie", "bollywood", "hollywood", "celebrity",
    "fashion", "music", "religion", "gossip", "horoscope", "recipe",
}


def _contains_keyword(text: str, keyword: str) -> bool:
    if " " in keyword:
        return keyword in text
    return bool(re.search(rf"\b{re.escape(keyword)}\b", text))


def evaluate_topic(title: str, summary: str = "", domain: str = "AI and Technology") -> dict[str, Any]:
    """Make the editorial gate explicit instead of publishing every RSS item."""

    text = f"{title} {summary}".lower().strip()

    for keyword in REJECT_KEYWORDS:
        if _contains_keyword(text, keyword):
            return {
                "publish": False,
                "score": 0,
                "reason": f"Rejected: outside the persona's technology scope ({keyword}).",
            }

    matches = [k for k in TECH_KEYWORDS if _contains_keyword(text, k)]

    if not matches:
        return {
            "publish": False,
            "score": 20,
            "reason": f"Rejected: insufficient evidence that the story is relevant to {domain}.",
        }

    change_words = (
        "launch", "release", "released", "update", "updated", "announce",
        "announced", "introduce", "introduced", "research", "researchers",
        "security", "vulnerability", "benchmark", "acquire", "acquisition",
        "open source", "model", "chip", "api",
    )
    change_signal = any(word in text for word in change_words)
    score = min(100, 55 + len(matches) * 7 + (15 if change_signal else 0))

    return {
        "publish": score >= 55,
        "score": score,
        "reason": (
            f"Selected: strong {domain} relevance ({', '.join(matches[:3])})"
            + (" and a concrete development signal." if change_signal else ".")
        ),
    }
