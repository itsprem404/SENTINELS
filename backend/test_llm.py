from services.llm_service import generate_post

post = generate_post(
    topic="OpenAI releases a new reasoning model.",
    persona_name="Nova",
    persona_domain="AI Product Analyst"
)

print(post)