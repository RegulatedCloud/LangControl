"""
"""
from typing import List, Callable, Any, Optional, TypeVar
from jinja2 import Environment, FileSystemLoader, select_autoescape

OutputModel = TypeVar("OutputModel")


class GenericPromptTemplateMixin:
    """Mixin for prompting and applying middlewares to the prompt_template"""

    env = Environment(
        loader=FileSystemLoader("prompt_templates"),
        autoescape=select_autoescape(),
    )

    def __init__(self, prompt_template: str = None):
        self.prompt_middlewares: List[Callable] = []
        self.prompt_template = prompt_template

    def get_rendered_prompt(self, prompt_template: str, **kwargs) -> str:
        template = self.env.get_template(f"{prompt_template}.jinja2")
        return template.render(**kwargs)

    def apply_prompt_middleware(self, prompt: str) -> str:
        """Apply middlewares to the prompt_template"""
        for middleware in self.prompt_middlewares:
            prompt = middleware(prompt)
        return prompt

    def apply(self, context: str) -> str:
        context = self.apply_prompt_middleware(prompt=context)
        prompt = self.get_rendered_prompt(prompt_template=self.prompt_template)

        if prompt is None:
            prompt = self.apply_prompt_middleware(prompt=context)
        else:
            prompt = self.apply_prompt_middleware(prompt=prompt)

        return prompt


class GenericStructuredOutputMixin:
    """Mixin for prompting and applying middlewares to the prompt_template and output model"""

    def __init__(
            self,
            output_model: Callable[[Any], OutputModel],
            prompt_template: Optional[Callable] = None,
    ):
        self.output_model = output_model
        self.prompt = prompt_template
        self.context_middlewares: List[Callable] = []
        self.model_middlewares: List[Callable] = []
        self.output_middlewares: List[Callable] = []

    def apply_context_middleware(self, **kwargs) -> {}:
        """Apply middlewares to the context"""
        context = {}
        for middleware in self.context_middlewares:
            context = middleware(**kwargs)
        return context

    def apply_model_middleware(self, output: OutputModel) -> OutputModel:
        """Apply middlewares to the structured output model"""
        for middleware in self.model_middlewares:
            output = middleware(output)
        return output

    def apply_output_middleware(
            self, context: str, prompt: str, output: OutputModel
    ) -> OutputModel:
        """Apply middlewares to the output"""
        if self.output_middlewares is not None:
            for middleware in self.output_middlewares:
                output = middleware(context, prompt, output)
        return output
