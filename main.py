"""Expose the FastAPI application and route requests to configured agents."""

import uvicorn
from fastapi import FastAPI, Request

from call_checker.main import reader

app = FastAPI(
    title="FastAPI Agent Server",
    description="An API for sending prompts to LangChain agents backed by Ollama.",
    version="0.1.0",
    summary="Prompt-driven LangChain agent API",
)


@app.post("/home")
async def home(request: Request):
    """Process an agent request submitted as a JSON HTTP payload."""
    data = await request.json()
    return reader(data)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
