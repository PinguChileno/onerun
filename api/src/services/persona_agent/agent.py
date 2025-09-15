from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import PromptTemplate

from src.utils.llm import get_llm

from .prompts import PROMPT_TEMPLATE
from .types import PersonaGeneration
from .dataset import generate_foundation


class PersonaAgent:
    """
    Agent responsible for generating persona attributes.

    Creates realistic character profiles, including background, personality
    traits, communication styles, and behavioral patterns.
    """

    llm: BaseChatModel

    def __init__(self):
        llm = get_llm("anthropic")
        self.llm = llm.with_structured_output(PersonaGeneration)

    async def generate_persona(self) -> PersonaGeneration:
        """
        Generate a complete persona with summary and attributes.

        Creates realistic persona characteristics including demographics,
        personality, communication style, and behavioral patterns.

        Returns: PersonaGeneration with summary and attributes
        """
        foundation = generate_foundation()

        prompt_template = PromptTemplate(
            template=PROMPT_TEMPLATE,
            template_format="jinja2",
            input_variables=["foundation"],
        )

        prompt = prompt_template.format(foundation=foundation)

        result = await self.llm.ainvoke(prompt)

        return result
