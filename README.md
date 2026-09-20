# fastapi-agent-server

A small FastAPI service that exposes LangChain agents through an HTTP endpoint. The
included `general` agent uses Ollama to run a local language model, so prompts can
be processed without sending them to a hosted model provider.

## How it works

1. FastAPI receives a JSON request at `POST /home`.
2. `call_checker.main.reader` selects an agent using the `agent` field.
3. The `general` agent sends the `prompt` to the configured Ollama model.
4. The server returns the agent's final response as a JSON string.

The application currently includes one functional agent, `general`. An unknown
agent name is returned as an informational string; it is not routed to Ollama.

## Requirements

- Python 3.13 or newer
- [`uv`](https://docs.astral.sh/uv/)
- [Ollama](https://ollama.com/)
- An Ollama model, `mistral` by default

Verify the tools are available:

```powershell
python --version
uv --version
ollama --version
```

## Installation

Clone the repository and enter its directory, then synchronize the environment
from the lock file:

```powershell
uv sync
```

Start Ollama if it is not already running and download the default model:

```powershell
ollama serve
ollama pull mistral
```

If Ollama is already running as a system service, only the `ollama pull` command
is needed.

## Configuration

The model name is read from the `OLLAMA_MODEL` environment variable. If it is not
set, the application uses `mistral`.

To use another model in PowerShell:

```powershell
$env:OLLAMA_MODEL = "llama3.2"
ollama pull llama3.2
```

The model must be installed in Ollama before the API receives a request. The
application connects to Ollama using its default local endpoint.

## Run the API

Start the development server from the project root:

```powershell
uv run python main.py
```

The server listens on `http://localhost:8000` and reloads when Python source files
change. The automatically generated API pages are available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI schema: `http://localhost:8000/openapi.json`

## API reference

### `POST /home`

Request body:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `agent` | string | Yes | Agent name. Use `general` for the included Ollama agent. |
| `prompt` | string | Yes | Non-empty text to send to the agent. |

Example request:

```json
{
	"agent": "general",
	"prompt": "Explain generative AI in 50 words."
}
```

PowerShell:

```powershell
Invoke-RestMethod `
		-Uri http://localhost:8000/home `
		-Method Post `
		-ContentType "application/json" `
		-Body '{"agent":"general","prompt":"Explain generative AI in 50 words."}'
```

Equivalent `curl` request:

```powershell
curl.exe -X POST http://localhost:8000/home `
		-H "Content-Type: application/json" `
		-d '{"agent":"general","prompt":"Explain generative AI in 50 words."}'
```

Successful responses contain the final text returned by the agent. For example,
if the prompt requests JSON, the HTTP response body is a JSON string whose content
may itself be JSON:

```json
"{\"Category\":\"technology\"}"
```

## Run the sample tester

The included tester reads text from `file_input.txt`, asks the `general` agent to
categorize it, and prints the `Category` value when the model returns valid JSON.

1. Create or edit `file_input.txt` in the project root.
2. Start the API in another terminal.
3. Run the tester:

```powershell
uv run python tester.py
```

The tester uses `http://localhost:8000/home` and waits up to 60 seconds for the
model response. It prints a connection message if the API is not running.

## Project layout

```text
main.py                 FastAPI application and /home route
agents/general.py       Ollama-backed LangChain agent
call_checker/main.py    Agent dispatch logic
tester.py               Sample classification client
file_input.txt          Local tester input, ignored by Git
pyproject.toml          Project metadata and dependencies
uv.lock                 Reproducible dependency lock file
```

## Adding an agent

To add another agent:

1. Create a module under `agents/` with a callable that accepts a prompt.
2. Import that callable in `call_checker/main.py`.
3. Add a branch for the new `agent` value in `reader`.
4. Document the new name and request behavior in this README.

## Troubleshooting

### The request cannot connect to Ollama

Make sure Ollama is running and the configured model is installed:

```powershell
ollama list
ollama run mistral
```

Stop the interactive model session after confirming it starts, then run the API
again.

### The tester cannot connect

Start the FastAPI server first with `uv run python main.py`, then run
`uv run python tester.py` from the project root.

### The model response is slow

The first request can take longer while Ollama loads the model. The tester allows
60 seconds, but larger models or limited hardware may need a longer client timeout.
