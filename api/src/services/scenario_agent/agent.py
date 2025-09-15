from textwrap import dedent
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import PromptTemplate

from src.services.persona_agent.agent import get_llm

from .types import PersonaContext
from .prompts import PROMPT_TEMPLATE


class ScenarioAgent:
    """
    Agent for generating scenario context (story and purpose) for personas
    within a simulation scenario using LLM.
    """

    llm: BaseChatModel

    def __init__(self):
        """
        Initialize the scenario agent with LLM.
        """
        llm = get_llm("anthropic")
        self.llm = llm.with_structured_output(PersonaContext)

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

    async def generate_context(
        self,
        scenario: str,
        agent_description: str,
        persona_attributes: dict[str, Any],
    ) -> PersonaContext:
        """
        Generate story and purpose for a persona within a simulation scenario.

        Args:
            scenario: The main simulation scenario
            agent_description: Description of what the agent does/helps with
            persona_attributes: The persona's attributes

        Returns: Generated context with story and purpose
        """
        persona_profile = self._format_profile(persona_attributes)

        prompt_template = PromptTemplate(
            template=PROMPT_TEMPLATE,
            template_format="jinja2",
            input_variables=[
                "scenario",
                "agent_description",
                "persona_profile",
            ],
        )

        prompt = prompt_template.format(
            scenario=scenario,
            agent_description=agent_description,
            persona_profile=persona_profile,
        )

        context: PersonaContext = await self.llm.ainvoke(prompt)

        return context
