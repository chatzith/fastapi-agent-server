"""Send a sample classification request to the local FastAPI application."""

import json

import requests

with open("file_input.txt", encoding="utf-8") as f:
    content = f.read().strip()

ENDPOINT = "http://localhost:8000/home"
DATA = {
    "agent": "general",
    "prompt": f"Categorize the following text: {content}. The response should be in JSON format with the key Category",
}


def main() -> None:
    """Submit the configured sample request and print the classification result."""
    try:
        response = requests.post(ENDPOINT, json=DATA, timeout=60)
        response.raise_for_status()
        result = response.json()
        if isinstance(result, str):
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                print(result)
                return

        if isinstance(result, dict):
            print(result.get("Category", result))
        else:
            print(result)
    except requests.exceptions.ConnectionError:
        print(f"Could not connect to {ENDPOINT}. Start the FastAPI server first.")
    except requests.exceptions.Timeout:
        print("The request timed out while waiting for the agent response.")
    except requests.exceptions.HTTPError as error:
        print(
            f"The API returned HTTP {error.response.status_code}: {error.response.text}"
        )
    except requests.exceptions.RequestException as error:
        print(f"The request failed: {error}")


if __name__ == "__main__":
    main()
