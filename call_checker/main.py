"""Select an agent from an incoming request and forward its prompt."""

from agents.general import run as run_general_agent


def reader(data: dict):
    """
    Read an agent request and call the selected agent.

    Args:
        data: Request data containing ``agent`` and ``prompt`` keys.

    Returns:
        The selected agent's response, or a message for an unknown agent.
    """
    agent = data["agent"]
    prompt = data["prompt"]

    if agent == "general":
        return run_general_agent(prompt)

    return f"You called the {agent} agent asking about '{prompt}'"
