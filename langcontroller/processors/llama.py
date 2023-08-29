"""Llama Index Processor Module.

This module contains the LlamaStructuredLLMOutput class, which is a
subclass of the LangController StructuredLLMOutputBase class.
"""
from dataclasses import dataclass

import pydantic
from llama_index.program import OpenAIPydanticProgram

from langcontroller.processors.base import (
    StructuredLLMOutputBase,
    OutputModel,
)


@dataclass
class LlamaStructuredLLMOutput(StructuredLLMOutputBase):
    """Llama Index Structured LLM Output."""

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

        program = OpenAIPydanticProgram.from_defaults(
            output_cls=self.output_model,
            verbose=True,
        )

        return program(prompt)
