"""Structured Output Strategy Abstract Base Class.

This module contains the Structured Output Strategy Abstract Base Class.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable

from jinja2 import Environment, FileSystemLoader, select_autoescape

from langcontroller.controllers import OutputModel


@dataclass
class StructuredOutputStrategy(ABC):
    """Structured Output Strategy Abstract Base Class."""

    prompt_template: str = field(default="")
    output_model: Callable[[str], OutputModel] = field(default_factory=OutputModel)

    @abstractmethod
    def apply(self, **kwargs) -> OutputModel:
        """Apply prompt_template then output model."""
        ...

    @staticmethod
    def get_rendered_prompt(prompt_template: str, **kwargs) -> str:
        """Get the rendered prompt_template.

        Args:
            prompt_template (str): The jinja2 template to use for the llm prompt
            **kwargs: The context to apply to the jinja2 template

        Returns:
            str: The rendered prompt_template
        """
        env = Environment(
            loader=FileSystemLoader("templates"),
            autoescape=select_autoescape(),
        )
        template = env.get_template(f"{prompt_template}.j2")
        return template.render(**kwargs)
