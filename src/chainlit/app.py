from chainlit import message

import chainlit as cl
from src.agents.orchestrator_agent import OrchestratorAgent

# Instantiate the orchestrator agent (could pass it env config if needed)
orchestrator = OrchestratorAgent()

@cl.on_chat_start
async def start():
    orchestrator.reset_session()

    await cl.Message(
        "👋 Hi there! Welcome to your Insurance Assistant. "
        "I can help you with your insurance plan, coverage questions, and find nearby hospitals. "
        "\n\nFirst, what’s your **name**?"
    ).send()


@cl.on_message
async def main_logic(user_message: message.Message):
    # Delegate handling to orchestrator agent
    bot_reply = await orchestrator.handle_message(user_message.content)
    # Send the orchestrator's reply to the user
    await cl.Message(content=bot_reply).send()
