AI_KEYWORDS = [
    "ai",
    "artificial intelligence",
    "machine learning",
    "llm",
    "gpt",
    "gemini",
    "claude",
    "openai",
    "anthropic",
    "google",
    "deepmind",
    "hugging face",
    "robotics",
    "python",
    "developer",
    "programming",
    "software",
    "github",
    "cybersecurity",
    "security"
]

REJECT_KEYWORDS = [
    "football",
    "cricket",
    "movie",
    "bollywood",
    "hollywood",
    "celebrity",
    "politics",
    "election",
    "murder",
    "crime",
    "fashion",
    "music",
    "religion"
]


def evaluate_topic(title: str, summary: str = ""):
    """
    Returns:
    {
        "publish": bool,
        "reason": str
    }
    """

    text = f"{title} {summary}".lower()

    # Reject unwanted topics
    for keyword in REJECT_KEYWORDS:
        if keyword in text:
            return {
                "publish": False,
                "reason": f"Rejected because it belongs to '{keyword}' category."
            }

    # Accept AI related topics
    for keyword in AI_KEYWORDS:
        if keyword in text:
            return {
                "publish": True,
                "reason": f"Relevant AI/Technology topic matched '{keyword}'."
            }

    return {
        "publish": False,
        "reason": "Not relevant to AI and Technology persona."
    }
