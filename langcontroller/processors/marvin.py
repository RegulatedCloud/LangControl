# -*- coding: utf-8 -*-
"""Marvin Controller Module.

This module contains the MarvinStructuredLLMOutput class, which is a
subclass of the StructuredLLMOutputBase class.
"""
from dataclasses import dataclass
from typing import Callable

import pydantic
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import InMemoryMetricReader
from loguru import logger

from langcontroller.processors.base import (
    StructuredLLMOutputBase,
    OutputModel,
)

metric_reader = InMemoryMetricReader()
provider = MeterProvider(metric_readers=[metric_reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)

prompt_render_counter = meter.create_counter(
    "prompt.render.counter",
    unit="1",
    description="Counts the number of times a prompt is rendered",
)

structured_llm_output_counter = meter.create_counter(
    "structured.llm.output.counter",
    unit="1",
    description="Counts the number of times a structured llm output completes successfully",
)

structured_llm_model_counter = meter.create_counter(
    "structured.llm.model.counter",
    unit="1",
    description="Counts the number of times a structured llm model is executed",
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

        def processor_filter() -> Callable[[], bool]:
            """Processor Filter.

            Returns:
                Callable[[], bool]: The filter function
            """

            def is_processor(record) -> bool:
                """Is Processor.

                Args:
                    record (dict): The loguru record

                Returns:
                    bool: True if the record is a processor, False otherwise
                """
                if all(
                    [
                        record.get("extra", False),
                        record["extra"].get("model", False),
                        record["extra"].get("prompt_template", False),
                    ]
                ):
                    return True

            return is_processor

        logger.add(
            f"logs/processors/{self.__class__.__name__}.log",
            rotation="10 MB",
            filter=processor_filter(),
            format="{time} | {level} | app.models.{extra[model]} | {extra[prompt_template]}.j2 | {message}",
        )
        context_logger = logger.bind(
            model=self.output_model.__name__, prompt_template=self.prompt_template
        )
        context_logger.debug("Applying MarvinStructuredLLMOutput...")

        context_logger.debug("Redering prompt_template...")
        prompt = self.get_rendered_prompt(
            prompt_template=self.prompt_template, **kwargs
        )
        context_logger.debug("Prompt rendered")
        prompt_render_counter.add(1, {"prompt.template": self.prompt_template})

        context_logger.debug("Submitting prompt to model for LLM processing...")
        output: OutputModel = self.output_model(prompt)
        context_logger.debug("Processing complete")
        for attribute in output.__fields__:
            context_logger.debug(
                f"{output.__class__.__name__}.{attribute}: {getattr(output, attribute)}"
            )

        structured_llm_model_counter.add(
            1, {"structured.llm.model": self.output_model.__name__}
        )

        structured_llm_output_counter.add(
            1, {"structured.llm.output": self.__class__.__name__}
        )
        return output
