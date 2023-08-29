"""LangController Base Classes.

This module contains the base classes of the LangController project.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, TypeVar, Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

OutputModel = TypeVar("OutputModel")
OutputModelStrategy = Callable[[Any], OutputModel]


@dataclass
class StructuredLLMOutputBase(ABC):
    """Structured Output Strategy Abstract Base Class."""

    output_model: OutputModelStrategy
    prompt_template: str = field(default="")

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
