import openai
from config import OPENAI_API_KEY, LLM_MODEL, LLM_TEMPERATURE

openai.api_key = OPENAI_API_KEY
_HAS_KEY = bool(OPENAI_API_KEY)

_FALLBACK_WORDS = [
    "Project", "Task", "Update", "Plan", "Draft", "Review", "Spec", "Checklist",
    "Iteration", "Milestone", "Deliverable", "Idea", "Sprint", "Backlog"
]

def _fallback_text(prompt: str) -> str:
    # Deterministic short text when no LLM is available
    h = abs(hash(prompt))
    w1 = _FALLBACK_WORDS[h % len(_FALLBACK_WORDS)]
    w2 = _FALLBACK_WORDS[(h // len(_FALLBACK_WORDS)) % len(_FALLBACK_WORDS)]
    return f"{w1} {w2}"

def generate_with_llm(prompt: str, temperature: float = LLM_TEMPERATURE) -> str:
    """Generate text using OpenAI API, or a local fallback if no API key is configured."""
    if not _HAS_KEY:
        return _fallback_text(prompt)
    try:
        response = openai.chat.completions.create(
            model=LLM_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"LLM generation error: {e}")
        return _fallback_text(prompt)

def generate_batch_with_llm(prompts: list[str]) -> list[str]:
    """Generate multiple items efficiently."""
    return [generate_with_llm(p) for p in prompts]