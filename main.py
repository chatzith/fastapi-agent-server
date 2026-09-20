"""Expose the FastAPI application and route requests to configured agents."""

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field

from call_checker.main import reader

app = FastAPI(
    title="FastAPI Agent Server",
    description="An API for sending prompts to LangChain agents backed by Ollama.",
    version="0.1.0",
    summary="Prompt-driven LangChain agent API",
)


class AgentRequest(BaseModel):
    """Parameters accepted by the agent execution endpoint."""

    agent: str = Field(
        description="Name of the agent to execute, for example 'general'.",
        examples=["general"],
    )
    prompt: str = Field(
        min_length=1,
        description="Non-empty prompt to send to the selected agent.",
        examples=["Explain generative AI in 50 words."],
    )


@app.post("/home")
async def home(request: AgentRequest):
    """Execute an agent with the supplied prompt."""
    return reader(request.model_dump())


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
