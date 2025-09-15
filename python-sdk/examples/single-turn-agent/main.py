import os

from dotenv import find_dotenv, load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    SystemMessage,
)

from onerun import Client
from onerun.types import ResponseInputItemParams, ResponseInputContentParams
from onerun.connect import RunConversationContext, WorkerOptions, run


load_dotenv(find_dotenv())


client = Client(
    base_url=os.getenv("ONERUN_API_BASE_URL"),
    api_key=os.getenv("ONERUN_API_KEY"),
)

llm = ChatAnthropic(model="claude-4-opus-20250514")


SYSTEM_PROMPT = """
You are a helpful customer service agent. Assist users with their questions and provide clear, accurate information.

CRITICAL: Respond with ONLY 1-2 short sentences. Keep responses brief and supportive.
"""


def create_agent_response(history: list[BaseMessage]) -> str:
    messages: list[BaseMessage] = [SystemMessage(content=SYSTEM_PROMPT)]
    messages.extend(history)

    output = llm.invoke(messages)

    # Get the output text
    content = output.content

    if isinstance(content, list):
        if not content:
            return ""

        item = content[0]

        if isinstance(item, dict):
            return item.get("text", "")  # type: ignore
        else:
            return item
    else:
        return content


async def entrypoint(ctx: RunConversationContext) -> None:
    """Handle a single-turn conversation between persona and agent."""
    print(f"Processing conversation: {ctx.conversation_id}")

    # Start conversation with agent greeting
    persona_response = client.simulations.conversations.responses.create(
        project_id=ctx.project_id,
        simulation_id=ctx.simulation_id,
        conversation_id=ctx.conversation_id,
        input=[ResponseInputItemParams(
            type="message",
            content=[ResponseInputContentParams(
                type="text",
                text="Hello! How can I assist you today?",
            )],
        )],
    )

    if persona_response.ended:
        return

    # Convert persona response to message format
    messages: list[BaseMessage] = []
    messages.extend([
        HumanMessage(
            content=[
                {
                    "type": content.type,
                    "text": content.text,
                }
                for content in item.content
            ],
        )
        for item in persona_response.output
    ])

    # Generate final agent response
    agent_response = create_agent_response(messages)

    # Send final response to complete the conversation
    client.simulations.conversations.responses.create(
        project_id=ctx.project_id,
        simulation_id=ctx.simulation_id,
        conversation_id=ctx.conversation_id,
        input=[ResponseInputItemParams(
            type="message",
            content=[ResponseInputContentParams(
                type="text",
                text=agent_response,
            )],
        )],
    )


if __name__ == "__main__":
    print("Starting worker")

    run(WorkerOptions(
        client=client,
        project_id=os.getenv("ONERUN_PROJECT_ID"),
        agent_id=os.getenv("ONERUN_AGENT_ID"),
        entrypoint=entrypoint,
    ))
