"""
AgentDesk – Groq Parser
Converts natural language IT requests into structured JSON tasks using Groq API.
Supports multi-step, multi-user requests.
"""

import os
import re
import json
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from project root .env
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# ---------------------------------------------------------------------------
# Configure Groq
# ---------------------------------------------------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise EnvironmentError(
        "GROQ_API_KEY not found. Please set it in the .env file at project root."
    )

client = Groq(api_key=GROQ_API_KEY)
# We will use a fast and reliable model
MODEL = "llama-3.3-70b-versatile"

# ---------------------------------------------------------------------------
# Prompt template
# ---------------------------------------------------------------------------
PROMPT_TEMPLATE = """You are an IT support assistant. Extract the list of actions and emails from the user's input.

Rules:
- You must return a LIST of tasks.
- Each task must have exactly two keys: "action" and "email".
- action must be one of: "create" or "reset"
- If the user says "create arpit@co.com and reset password for bob@co.com", you must return TWO tasks.
- If the user says "create and reset password for arpit@co.com", you must return TWO tasks (both for arpit@co.com).
- email must be a valid email address.

User input: "{user_input}"

Return ONLY valid JSON in this exact format, nothing else:
{{
  "tasks": [
    {{"action": "create", "email": "user1@example.com"}},
    {{"action": "reset", "email": "user2@example.com"}}
  ]
}}
"""

def safe_parse(response_text: str) -> dict:
    """Robust JSON parsing with regex fallback."""
    try:
        # First try parsing the whole thing directly
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass
    
    # Extract just the JSON block using a robust regex
    match = re.search(r"\{.*\}", response_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    
    raise ValueError("Could not extract valid JSON from response.")


def parse_input(user_input: str) -> dict:
    """
    Parse natural language IT request into a dictionary containing a list of tasks.
    """
    prompt = PROMPT_TEMPLATE.format(user_input=user_input)

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=MODEL,
            temperature=0, 
        )
        raw_text = response.choices[0].message.content.strip()
        
        result = safe_parse(raw_text)
        
        if "tasks" in result and isinstance(result["tasks"], list):
            # Validate each task
            for t in result["tasks"]:
                if "action" not in t or "email" not in t:
                    raise ValueError(f"Invalid task structure in: {t}")
            return result
        else:
            raise ValueError("Expected a 'tasks' list in JSON response.")

    except Exception as e:
        raise ValueError(f"Failed to parse input: {e}")


# ---------------------------------------------------------------------------
# CLI test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python llm_parser.py \"create user john@company.com and reset bob@co.com\"")
        sys.exit(1)

    user_input = " ".join(sys.argv[1:])
    print(f"📝 Input: {user_input}")
    result = parse_input(user_input)
    print(f"✅ Parsed: {json.dumps(result, indent=2)}")
