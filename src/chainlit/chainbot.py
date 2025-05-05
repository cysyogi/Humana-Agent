import json
from pathlib import Path

import chainlit as cl

from src.query.query_data import query_rag, BASE_K

POLICY_MAP_PATH = Path("data") / "policy_mapping.json"
POLICY_MAPPING: dict[str, str] = json.loads(POLICY_MAP_PATH.read_text())


def _resolve_policy(user_input: str) -> str | None:
    """Return a policy_id (collection name) or None if not found."""
    if user_input in POLICY_MAPPING:
        return user_input
    for pid, name in POLICY_MAPPING.items():
        if name.lower() == user_input.lower():
            return pid
    return None


# -----------------------------------------------------------------
#  Chainlit lifecycle
# -----------------------------------------------------------------
@cl.on_chat_start
async def chat_start():
    cl.user_session.set("stage", "need_name")
    await cl.Message("Hi! 👋 What’s your **name**?").send()


@cl.on_message
async def chat(msg: cl.Message):
    stage = cl.user_session.get("stage", "ready")

    # 1️⃣ Collect name
    if stage == "need_name":
        cl.user_session.set("name", msg.content.strip())
        cl.user_session.set("stage", "need_zip")
        await cl.Message("Nice to meet you! What’s your **ZIP code**?").send()
        return

    # 2️⃣ Collect ZIP
    if stage == "need_zip":
        cl.user_session.set("zip", msg.content.strip())
        cl.user_session.set("stage", "need_policy")
        await cl.Message("Please enter your **policy number** or **policy name**.").send()
        return

    # 3️⃣ Collect policy
    if stage == "need_policy":
        policy_id = _resolve_policy(msg.content.strip())
        if policy_id is None:
            await cl.Message("❌ I couldn’t find that policy. Try again.").send()
            return

        cl.user_session.set("policy_id", policy_id)
        cl.user_session.set("stage", "ready")
        await cl.Message(
            f"Great! You can now ask questions about "
            f"**{POLICY_MAPPING[policy_id]}**."
        ).send()
        return

    # 4️⃣ Answer questions using RAG
    policy_id = cl.user_session.get("policy_id")
    if policy_id is None:  # user skipped setup somehow
        cl.user_session.set("stage", "need_policy")
        await cl.Message("Please tell me your policy number first.").send()
        return

    answer = query_rag(msg.content, policy_id, k=BASE_K)
    await cl.Message(answer).send()
