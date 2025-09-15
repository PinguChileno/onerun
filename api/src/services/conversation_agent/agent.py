import logging
from textwrap import dedent
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)
from langchain_core.prompts import PromptTemplate

from src.utils.llm import get_llm

from .prompts import PROMPT_TEMPLATE


class ConversationAgent:
    """
    Agent for simulating realistic user conversations based on personas and
    scenarios.

    Embodies a specific persona with scenario-specific context to interact
    naturally with AI agents, providing authentic testing of conversational AI
    systems.
    """

    logger: logging.Logger = logging.getLogger("ConversationAgent")

    llm: BaseChatModel

    def __init__(self):
        self.llm = get_llm("anthropic")

    def _format_profile(self, attributes: dict[str, Any]) -> str:
        age_group = attributes.get("age_group", "not specified")
        education = attributes.get("education", "not specified")
        occupation = attributes.get("occupation", "not specified")
        economic_status = attributes.get("economic_status", "not specified")
        personality_traits = attributes.get(
            "personality_traits",
            "not specified",
        )
        values = attributes.get("values", "not specified")
        interests = attributes.get("interests", "not specified")
        speech_style = attributes.get("speech_style", "not specified")
        speech_patterns = attributes.get("speech_patterns", "not specified")
        typical_behavior = attributes.get("typical_behavior", "not specified")
        stress_triggers = attributes.get("stress_triggers", "not specified")
        stress_reactions = attributes.get("stress_reactions", "not specified")

        template = dedent("""
            Age Group: {age_group}
            Education: {education}
            Occupation: {occupation}
            Economic Status: {economic_status}
            Personality Traits: {personality_traits}
            Values: {values}
            Interests: {interests}
            Speech Style: {speech_style}
            Speech Patterns: {speech_patterns}
            Typical Behavior: {typical_behavior}
            Stress Triggers: {stress_triggers}
            Stress Reactions: {stress_reactions}
        """)

        return template.format(
            age_group=age_group,
            education=education,
            occupation=occupation,
            economic_status=economic_status,
            personality_traits=personality_traits,
            values=values,
            interests=interests,
            speech_style=speech_style,
            speech_patterns=speech_patterns,
            typical_behavior=typical_behavior,
            stress_triggers=stress_triggers,
            stress_reactions=stress_reactions,
        )

    def _create_system_prompt(
        self,
        agent_description: str,
        persona_attributes: dict[str, Any],
        persona_story: str,
        persona_purpose: str,
        max_turns: int,
    ) -> str:
        """Create the system prompt with all persona and context details"""
        persona_profile = self._format_profile(persona_attributes)

        prompt_template = PromptTemplate(
            template=PROMPT_TEMPLATE,
            template_format="jinja2",
            input_variables=[
                "agent_description",
                "persona_profile",
                "persona_story",
                "persona_purpose",
                "max_turns",
            ],
        )

        return prompt_template.format(
            agent_description=agent_description,
            persona_profile=persona_profile,
            persona_story=persona_story,
            persona_purpose=persona_purpose,
            max_turns=max_turns,
        )

    def _create_message_history(
        self,
        history: list[dict[str, Any]],
    ) -> list[BaseMessage]:
        """Convert history to LangChain message format"""
        messages: list[BaseMessage] = []

        for message in history:
            role = message.get("role", "user")
            content = message.get("content", "")

            # Invert roles:
            #   DB 'user' = persona said it = AIMessage
            #   DB 'assistant' = agent being tested said it = HumanMessage
            if role == "user":  # persona message in DB
                messages.append(AIMessage(content=content))
            elif role == "assistant":  # agent being tested message in DB
                messages.append(HumanMessage(content=content))
            # Skip system messages from history - we'll add our own

        return messages

    def _should_initiate_conversation(
        self,
        history: list[dict[str, Any]],
    ) -> bool:
        """Check if this persona should start the conversation"""
        return len(history) == 0

    async def generate_reply(
        self,
        agent_description: str,
        persona_attributes: dict[str, Any],
        persona_story: str,
        persona_purpose: str,
        max_turns: int,
        history: list[dict[str, Any]],
    ) -> str:
        """Generate a response as this persona"""
        try:
            # Create the system prompt
            system_prompt = self._create_system_prompt(
                agent_description=agent_description,
                persona_attributes=persona_attributes,
                persona_story=persona_story,
                persona_purpose=persona_purpose,
                max_turns=max_turns,
            )

            # Create the message list
            messages: list[BaseMessage] = [
                SystemMessage(content=system_prompt),
            ]

            if self._should_initiate_conversation(history):
                # Persona initiates the conversation
                messages.append(HumanMessage(
                    content=(
                        "[Start the conversation based on "
                        "your individual story]"
                    ),
                ))
            else:
                # Convert conversation history
                history_messages = self._create_message_history(history)
                messages.extend(history_messages)
                # The last message should be from the agent being tested,
                # persona responds to it

            output = await self.llm.ainvoke(messages)

            content = output.content

            if isinstance(content, list):
                if len(content) > 0:
                    item = content[0]
                    if isinstance(item, dict):
                        text = item.get("text", "")  # type: ignore
                    else:
                        text = item
                else:
                    text = ""
            else:
                text = content

            return text

        except Exception as e:
            self.logger.error(f"Error occurred while generating reply: {e}")
            raise
