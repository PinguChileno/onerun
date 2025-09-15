import logging
from textwrap import dedent
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from pydantic import Field, BaseModel

from src.utils.llm import get_llm

from .prompts import SYSTEM_PROMPT_TEMPLATE, USER_PROMPT_TEMPLATE


class Evaluation(BaseModel):
    objective_id: str = Field(..., description="Objective ID")
    score: float = Field(..., description="Objective score")
    reason: str = Field(..., description="Reason for the score")


class EvaluationsResult(BaseModel):
    evaluations: list[Evaluation]


class EvalAgent:
    """
    Agent for evaluating conversation quality against defined objectives using
    LLM.

    Takes conversation history and evaluation objectives, then provides scored
    analysis of how well the conversation met each objective.
    """

    logger: logging.Logger = logging.getLogger("EvalAgent")

    llm: BaseChatModel

    def __init__(self):
        llm = get_llm("anthropic")
        self.llm = llm.with_structured_output(EvaluationsResult)

    def _format_conversation(self, history: list[dict[str, Any]]) -> str:
        """Format conversation history as a readable string"""
        conversation_lines: list[str] = []

        for i, message in enumerate(history, 1):
            role = message.get("role", "user").upper()
            content = message.get("content", [])

            # Extract text from content blocks
            text_parts = []
            for block in content:
                if block["type"] != "text":
                    continue

                # For now only text blocks are considered
                text_parts.append(block["text"])

            text = "\n".join(text_parts).strip()

            if text:
                conversation_lines.append(f"Turn {i} - {role}: {text}")

        return "\n\n".join(conversation_lines)

    def _format_objectives(self, objectives: list[dict[str, Any]]) -> str:
        """Format objectives as a readable string"""
        objectives_text: list[str] = []

        for obj in objectives:
            obj_text = dedent(f"""
                ID: {obj['id']}
                Name: {obj['name']}
                Criteria: {obj.get('criteria', [])}
            """)

            objectives_text.append(obj_text)

        return "\n\n---\n\n".join(objectives_text)

    async def evaluate(
        self,
        objectives: list[dict[str, Any]],
        history: list[dict[str, Any]],
    ) -> EvaluationsResult:
        """
        Evaluate conversation against objectives

        Args:
            objectives: List of objectives
                [{"id": "...", "name": "...", "criteria": "..."}]
            history: Conversation history in format
                [{"role": "user/assistant", "content": [...]}]

        Returns:
            List of evaluations
        """
        formatted_conversation = self._format_conversation(history)
        formatted_objectives = self._format_objectives(objectives)

        system_prompt_template = PromptTemplate(
            template=SYSTEM_PROMPT_TEMPLATE,
            template_format="jinja2",
            input_variables=[],
        )
        system_prompt = system_prompt_template.format()

        user_prompt_template = PromptTemplate(
            template=USER_PROMPT_TEMPLATE,
            template_format="jinja2",
            input_variables=["objectives", "conversation"],
        )
        user_prompt = user_prompt_template.format(
            objectives=formatted_objectives,
            conversation=formatted_conversation
        )

        messages: list[BaseMessage] = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]

        return await self.llm.ainvoke(messages)
