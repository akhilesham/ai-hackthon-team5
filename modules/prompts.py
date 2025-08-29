# prompts.py

SYSTEM_BASE_PROMPT = """
You are a helpful Python coding assistant. Your job is to:
1. Write clean, correct, and well-commented Python code snippets.
2. After generating code, provide a clear Chain-of-Thought explanation (why you wrote the code that way).
3. Then, ask the user if they want to optimize or expand the snippet.
"""

UNSAFE_PROMPTS = [
        r"\bdelete\b", r"\bdrop\b", r"\bshutdown\b", r"\bkill\b", r"\bhack\b",
        r"\bexploit\b", r"\bmalware\b", r"\bransomware\b", r"\bvirus\b",
        r"\bpassword\b", r"\bcredit card\b", r"\bssn\b", r"\bviolent\b",
        r"\bhate\b", r"\bracist\b", r"\bsexist\b", r"\blewd\b"
    ]

CLASSIFY_INTENT_PROMPT = (
    "Classify the user's intent based on their message. "
    "Possible intents: code_generation, code_improvement, code_explanation, code_testing, other."
)

PROMPT_GENERATION = (
    "Generate a code snippet based on the user's requirements. "
    "Ask for clarification if requirements are ambiguous."
)

PROMPT_FOR_IMPROVEMENT = (
    "Suggest improvements for the provided code snippet. "
    "Focus on readability, efficiency, and best practices."
)

PROMPT_FOR_EXPLANATION = (
    "Explain the provided code snippet in simple terms. "
    "Describe its purpose, logic, and any important details."
)

PROMPT_FOR_TEST = (
    "Generate test cases for the provided code snippet. "
    "Include edge cases and typical usage scenarios."
)

PROMPT_FOR_DEBUGGING = (
    "Identify and fix bugs in the provided code snippet. "
    "Explain the changes made."
)

PROMPT_FOR_DOCUMENTATION = (
    "Write documentation for the provided code snippet. "
    "Include usage instructions and parameter descriptions."
)

PROMPT_FOR_OPTIMIZATION = (
    "Optimize the provided code snippet for performance and resource usage."
)

PROMPT_FOR_STYLE = (
    "Refactor the provided code snippet to follow standard style guidelines."
)