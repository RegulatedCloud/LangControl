"""Marvin Structured Output Strategy.

MarvinAI specific Strategy for submitting prompts to Marvin
"""
from dataclasses import dataclass

from langcontroller.controllers.structs import OutputModel
from langcontroller.controllers.generic import (
    StructuredOutputStrategy,
)


@dataclass
class MarvinStructuredOutputStrategy(StructuredOutputStrategy):
    """A MarvinAI specific Mixin for structured output."""

    def apply(self, **kwargs) -> OutputModel:
        """Apply prompt_template then output model.

        Args:
            **kwargs: The context to apply to the jinja2 template for the llm prompt_template

        Returns:
            OutputModel: The populated structured output model based on Pydantic
        """
        prompt = self.get_rendered_prompt(
            prompt_template=self.prompt_template, **kwargs
        )

        return self.output_model(prompt)
