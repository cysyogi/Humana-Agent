import json
from pathlib import Path

from src.services.openai_service import ask_openai

POLICY_MAP_PATH = Path("data") / "policy_mapping.json"

def load_policy_mapping() -> dict[str, str]:
    """
    Reads the mapping from disk each time so changes show up immediately.
    """
    if not POLICY_MAP_PATH.exists():
        return {}
    return json.loads(POLICY_MAP_PATH.read_text())


def resolve_policy(user_input: str):
    """
    Resolve user input to policy id.

    Returns:
        policy_id (str or None): if found
        exact (bool): True if exact, False if assumed
    """

    # Exact match by ID
    if user_input in load_policy_mapping():
        return user_input, True

    # Exact match by name (case insensitive)
    for pid, name in load_policy_mapping().items():
        if name.lower() == user_input.lower():
            return pid, True

    # Use LLM to resolve
    policies_text = "\n".join([f"{pid}: {name}" for pid, name in load_policy_mapping().items()])

    prompt = f"""
    Available Policies:
    
    {policies_text}
    
    User input: {user_input}
    
    Which policy does this refer to? 
    If confident, return ONLY the policy ID exactly. 
    If unsure, return "None".
    """

    response = ask_openai(prompt)

    if response == "None":
        return None, False

    return response, response in load_policy_mapping()
