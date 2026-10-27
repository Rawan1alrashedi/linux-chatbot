
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load API key from .env
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise ValueError(
        "API key is missing. Check your .env file."
    )

# Connect to Claude API
client = Anthropic(api_key=api_key)

# Linux specialist instructions
SYSTEM_PROMPT = """
You are Linux AI Assistant, a specialist in Linux
and Linux system administration.

Your responsibilities:
- Explain Linux commands and terminal usage.
- Help with files, directories, permissions, and users.
- Explain processes, CPU, memory, and services.
- Help troubleshoot networking and connectivity.
- Explain system logs and error messages.
- Help with package management and shell scripting.
- Provide practical examples and step-by-step guidance.

Rules:
- Answer Linux-related questions only.
- If a question is unrelated to Linux, politely explain
  that your specialty is Linux.
- Respond in the same language as the user.
- Explain what commands do before suggesting them.
- Never claim you executed commands on the user's machine.
- Never invent command output or claim server access.
- Ask which Linux distribution is being used when relevant.
- Warn users before destructive or risky commands.
- Prefer safe, read-only diagnostic commands first.
- Never ask users to share passwords or API keys.
"""

print("=" * 40)
print("       Linux AI Assistant")
print("       Powered by Claude")
print("=" * 40)
print("Ask me anything about Linux.")
print("Type 'exit' to quit.\n")

while True:
    try:
        question = input("You: ").strip()

        if question.lower() == "exit":
            print("Linux AI Assistant: Goodbye!")
            break

        if not question:
            continue

        response = client.messages.create(
            model="claude-haiku-4-5",
            max_tokens=700,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": question
                }
            ],
        )

        answer = "".join(
            block.text
            for block in response.content
            if block.type == "text"
        )

        print(f"\nLinux AI Assistant: {answer}\n")

    except KeyboardInterrupt:
        print("\nLinux AI Assistant: Goodbye!")
        break

    except Exception as error:
        print(f"\nRequest failed: {error}\n")
