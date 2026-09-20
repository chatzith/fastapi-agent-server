"""Configure and run the general-purpose Ollama-backed agent."""

import os

from langchain.agents import create_agent
from langchain_ollama import ChatOllama

MODEL_NAME = os.getenv("OLLAMA_MODEL", "mistral")
SYSTEM_PROMPT = (
    "You are a helpful and precise assistant. Answer the user's request directly. "
    "Follow any requested output format exactly, including JSON when requested."
)

model = ChatOllama(model=MODEL_NAME)
agent = create_agent(model=model, system_prompt=SYSTEM_PROMPT)


def run(prompt: str) -> str:
    """Run the general agent with a non-empty prompt and return its response."""
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt must be a non-empty string")

    result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    messages = result.get("messages", [])
    if not messages:
        raise RuntimeError("The agent returned no messages")

    return messages[-1].content
