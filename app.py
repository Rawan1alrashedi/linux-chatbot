
import os
import streamlit as st
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

st.set_page_config(
    page_title="Linux AI Assistant",
    page_icon="🐧",
    layout="centered",
)

SYSTEM_PROMPT = """
You are Linux AI Assistant, a specialist in Linux
and Linux system administration.

Help with:
- Linux commands and terminal usage
- Files, directories, permissions, and users
- Processes, CPU, memory, and services
- Networking and troubleshooting
- System logs and error messages
- Package management and shell scripting

Rules:
- Answer Linux-related questions only.
- Politely decline unrelated questions.
- Respond in the same language as the user.
- Explain commands and provide practical examples.
- Never claim to execute commands on the user's machine.
- Never invent command output or claim server access.
- Ask which Linux distribution is used when relevant.
- Warn before destructive or risky commands.
- Prefer safe diagnostic commands first.
- Never ask for passwords or API keys.
"""

st.title("🐧 Linux AI Assistant")
st.caption("Your personal assistant for Linux commands and troubleshooting")

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    st.error("API key missing. Check your .env file.")
    st.stop()

client = Anthropic(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question = st.chat_input("Ask me anything about Linux...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.messages.create(
                    model="claude-haiku-4-5",
                    max_tokens=1000,
                    system=SYSTEM_PROMPT,
                    messages=[
                        {
                            "role": message["role"],
                            "content": message["content"],
                        }
                        for message in st.session_state.messages
                    ],
                )

                answer = "".join(
                    block.text
                    for block in response.content
                    if block.type == "text"
                )

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                    }
                )

            except Exception as error:
                st.error(f"Request failed: {error}")
