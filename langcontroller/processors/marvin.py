"""Marvin Controller Module.

This module contains the MarvinController class, which is a subclass of
the LangController class.
"""
from dataclasses import dataclass

import pydantic

from langcontroller.processors.base import (
    StructuredLLMOutputBase,
    OutputModel,
)


@dataclass
class MarvinStructuredLLMOutput(StructuredLLMOutputBase):
    """Marvin Structured LLM Output."""

    def apply(self, **kwargs) -> OutputModel:
        """Apply prompt_template then output pydantic model.

        Args:
            **kwargs: The context to apply to the jinja2 template for the llm prompt_template

        Returns:
            `pydantic.main.ModelMetaclass`: The output model
        """
        prompt = self.get_rendered_prompt(
            prompt_template=self.prompt_template, **kwargs
        )

        return self.output_model(prompt)
