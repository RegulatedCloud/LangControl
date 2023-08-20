from typing import List, Callable, Any, TypeVar

from langcontroller.controllers.generic import GenericPromptTemplateMixin, GenericStructuredOutputMixin

OutputModel = TypeVar("OutputModel")


class MarvinStructuredOutputController(
    GenericPromptTemplateMixin, GenericStructuredOutputMixin
):
    """A MarvinAI specific Mixin for prompting and applying middlewares to the prompt_template and output model"""

    def __init__(
            self,
            output_model: Callable[[Any], OutputModel],
            prompt_template: str = None,
    ):
        super().__init__()
        self.output_model = output_model
        self.prompt_template = prompt_template
        self.context_middlewares: List[Callable] = []
        self.prompt_middlewares: List[Callable] = []
        self.model_middlewares: List[Callable] = []
        self.output_middlewares: List[Callable] = []

    def apply(self, **kwargs) -> OutputModel:
        context = self.apply_context_middleware(**kwargs)

        prompt = self.get_rendered_prompt(
            prompt_template=self.prompt_template, **kwargs
        )
        prompt = self.apply_prompt_middleware(prompt=prompt)

        model = self.apply_model_middleware(output=self.output_model)
        model = model(prompt)
        output = self.apply_output_middleware(
            context=context, prompt=prompt, output=model
        )
        return output
