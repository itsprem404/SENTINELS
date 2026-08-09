# By reading all these prompts you all will think we made whole thing with just ai but trust me it's not just ai, Yes we did made whole backend structure by chatgpt but we changed everything by the time when we started making good database and frontend!! (Because of Frontend We had to modify most of the Backend)... And This is not the Only Chat we have done but it's difficult to add every chat so we added the biggest one.



Claim offer

Friday 10:55 AM
hi

Hi! 👋 How can I help you today?


dyk breeth ai?

Do you mean Breeth AI?

If so, I don't know of a major, widely recognized AI product by that exact name. It could be:

A newer AI startup or app.

A niche tool that isn't widely known.

A typo (for example, "Breathe AI," "Breath AI," or something similar).

If you can share:

the website,

a screenshot,

or tell me what it does,

I'll explain it or help you compare it with other AI tools.


885d652c-7ceb-4f2e-a3c9-cb2f56876b2d.png

Yes! From your screenshot, this is Breeth (the website is thebreeth.com), not "Breeth AI."

Based on what I can see, Breeth is an intent-aware memory platform for AI agents. The headline says:

"Breeth knows why, what, how."

Their main idea is that instead of storing only facts, Breeth stores:

Why something is true (the reasoning)

What the canonical fact is

How it should be used or interpreted

This helps multiple AI agents or applications stay consistent instead of gradually giving different answers.

What it does
Breeth acts as a shared memory layer for AI applications.

Normally:

User
   ↓
LLM
   ↓
Vector DB / RAG
With Breeth:

User
   ↓
LLM
   ↓
Breeth Memory
   ├── Facts
   ├── Intent
   ├── Reasoning
   ├── Relationships
   └── Context
So if your AI assistant learns:

Company refund policy

Coding standards

User preferences

Product documentation

Breeth remembers why those decisions were made, not just the text itself.

Who it's for
It seems targeted at developers building:

AI assistants

Customer support bots

Multi-agent systems

Coding agents

Enterprise AI applications

rather than end users.

Why it's different from a vector database
A normal vector database (Pinecone, Chroma, Weaviate, etc.) retrieves documents based on semantic similarity.

Breeth is trying to provide:

Persistent memory

Relationships between facts

Intent tracking

Canonical ("single source of truth") knowledge

Consistent responses across different agents

Is it an LLM?
No.

Breeth isn't a model like GPT, Claude, or Gemini.

It's infrastructure that sits behind those models to improve memory and consistency.

Should you use it?
If you're building:

AI SaaS

AI agents

MCP servers

Enterprise copilots

Long-term memory assistants

then it's an interesting technology to explore. If you're just chatting with AI or building a simple chatbot, it's probably more than you need.

If you're interested, I can also explain how Breeth compares with OpenAI Memory, LangGraph Memory, Mem0, and vector databases like Pinecone—that's where the differences become much clearer.


da7a7c81-6333-4a37-9df4-57cb9844222b.png

60d46130-8d28-45f2-8b57-f0c0dfeccfbb.png

08e69355-7536-4c46-84c9-f50f44bd5beb.png
Should I change the name and the domain If yes then how?

c06d002b-d45d-4afe-9ef7-904f60b923ab.png

2e65e985-fbda-4445-b75c-a76e52540742.png

a7fe0ea7-6602-4ac2-8d95-7815f8a1cc3c.png


Pasted markdown.md
File
Kuch posts bhej raha hu check karo 



backend.zip
Zip Archive
yeh rahi backend ki zip

Okay — ab ek important clue mil gaya.

Agar exact string:

[https://openai.com/index/hsp-gruppe](https://openai.com/index/hsp-gruppe)
function ko dene par bhi same output aa raha hai, toh jo function hum edit kar rahe hain woh actual runtime me expected code execute nahi kar raha. Hum ab aur code blindly change nahi karenge.

Ab ye 2 commands chalao
1. Function ka actual source:

python -c "import inspect; from agent.publisher import normalize_source_url; print(inspect.getsource(normalize_source_url))"
2. Python kis publisher.py ko load kar raha hai:

python -c "import agent.publisher; print(agent.publisher.__file__)"
Expected
Second command ideally:

D:\Hackathon\SENTINELS\backend\agent\publisher.py
Aur first command me exactly wahi latest function dikhna chahiye jo humne abhi paste kiya:

if source.startswith("[") and "](" in source:
    url = source.split("](", 1)[1]

    if url.endswith(")"):
        url = url[:-1]

    return url.strip()
Dono outputs paste karo.
Uske baad main exact issue identify karunga—abhi publisher.py me aur changes mat karo.


$ python -c "import inspect; from agent.publisher import normalize_source_url; print(inspect.getsource(normalize_source_url))"
def normalize_source_url(source: str) -> str:
"""
Return a plain URL even if an upstream source is Markdown-formatted.
"""

if not source:
    return ""

source = source.strip()

# Convert:
# [https://example.com](https://example.com)
# into:
# https://example.com
match = re.fullmatch(
    r"\[.*?\]\((https?://[^)]+)\)",
    source
)

if match:
    return match.group(1).strip()

return source
niche@RISHI MINGW64 /d/Hackathon/SENTINELS/backend (main)
$ python -c "import agent.publisher; print(agent.publisher.file)"
D:\Hackathon\SENTINELS\backend\agent\publisher.py


Perfect — ab root cause 100% clear hai. ✅

Python correct file load kar raha hai:

D:\Hackathon\SENTINELS\backend\agent\publisher.py
Lekin us file ke andar abhi bhi purana regex function hi saved hai:

match = re.fullmatch(
    r"\[.*?\]\((https?://[^)]+)\)",
    source
)
Isliye previous replacement actually file me save nahi hua tha.

Ab exact fix
backend/agent/publisher.py kholo.

Is poore function ko:

def normalize_source_url(source: str) -> str:
    """
    Return a plain URL even if an upstream source is Markdown-formatted.
    """

    if not source:
        return ""

    source = source.strip()

    match = re.fullmatch(
        r"\[.*?\]\((https?://[^)]+)\)",
        source
    )

    if match:
        return match.group(1).strip()

    return source
delete karke exactly ye paste karo:

def normalize_source_url(source: str) -> str:
    """
    Convert Markdown links into plain URLs.
    """

    if not source:
        return ""

    source = source.strip()

    # Markdown link: [label](https://example.com)
    if source.startswith("[") and "](" in source:
        url = source.split("](", 1)[1]

        if url.endswith(")"):
            url = url[:-1]

        return url.strip()

    return source
Top par
Ye line:

import re
ab delete kar sakte ho, kyunki new function regex use nahi karta.

Save karna mat bhoolna
Ctrl + S 🔴

Phir verify:

python -c "import inspect; from agent.publisher import normalize_source_url; print(inspect.getsource(normalize_source_url))"
Output me source.startswith("[") dikhna chahiye.

Uske baad:

python -c "from agent.publisher import normalize_source_url; x='[https://openai.com/index/hsp-gruppe](https://openai.com/index/hsp-gruppe)'; print(normalize_source_url(x))"
Expected:

https://openai.com/index/hsp-gruppe
Abhi server start mat karo. Pehle ye last command ka output check karte hain.


$ python -c "import inspect; from agent.publisher import normalize_source_url; print(inspect.getsource(normalize_source_url))"
def normalize_source_url(source: str) -> str:
"""
Return a plain URL even if an upstream source is Markdown-formatted.
"""

if not source:
    return ""

source = source.strip()

# Convert:
# [https://example.com](https://example.com)
# into:
# https://example.com
match = re.fullmatch(
    r"\[.*?\]\((https?://[^)]+)\)",
    source
)

if match:
    return match.group(1).strip()

return source
niche@RISHI MINGW64 /d/Hackathon/SENTINELS/backend (main)
$ python -c "from agent.publisher import normalize_source_url; x='https://openai.com/index/hsp-gruppe'; print(normalize_source_url(x))"
https://openai.com/index/hsp-gruppe


Haan, ab definitely confirm ho gaya: publisher.py me change save hi nahi hua. Python abhi bhi purana regex function load kar raha hai.

Is baar editor me manually replace karne ke bajay Git Bash se directly file ko modify kar dete hain, taaki save issue na ho.

1. agent/publisher.py kholo
notepad agent/publisher.py
Notepad me old function:

def normalize_source_url(source: str) -> str:
    """
    Return a plain URL even if an upstream source is Markdown-formatted.
    """

    if not source:
        return ""

    source = source.strip()

    match = re.fullmatch(
        r"\[.*?\]\((https?://[^)]+)\)",
        source
    )

    if match:
        return match.group(1).strip()

    return source
ko completely delete karke ye paste karo:

def normalize_source_url(source: str) -> str:
    """
    Convert Markdown links into plain URLs.
    """

    if not source:
        return ""

    source = source.strip()

    if source.startswith("[") and "](" in source:
        url = source.split("](", 1)[1]

        if url.endswith(")"):
            url = url[:-1]

        return url.strip()

    return source
Ctrl + S → Notepad close.

2. Ab verify karo
python -c "import inspect; from agent.publisher import normalize_source_url; print(inspect.getsource(normalize_source_url))"
Isme ab ye line must dikhni chahiye:

if source.startswith("[") and "](" in source:
Agar ab bhi re.fullmatch dikh raha hai, to file save/replace nahi hui.

3. Phir actual test
python -c "from agent.publisher import normalize_source_url; x='[https://openai.com/index/hsp-gruppe](https://openai.com/index/hsp-gruppe)'; print(normalize_source_url(x))"
Expected:

https://openai.com/index/hsp-gruppe
Bas is test ka output bhejo. Uske baad hum new post generate karke database verify karenge.


