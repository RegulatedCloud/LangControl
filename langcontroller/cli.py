"""A Generative AI Python Application Framework.

Inspiration:
    Django, Laravel, and Meltano

Features:
    Architected for both Human and AI Devs
    Scaffolds are designed to help your AI Code Assistant
    Generated components render with CLI, FastAPI, and Dagster

Template Naming Conventions:
    <domain>_<operation>_<data_type>
    domain - manage|models|pipeline|prompt_templates|pyproject|features
    operation - append|create
    data_type - asset|class|function|file|prompt|sensor
"""
import os
from enum import Enum
from typing_extensions import Annotated

from rich import print

import typer

from langcontroller.utils import Renamer, TemplateWriter, Commandify

app = typer.Typer(rich_markup_mode="rich")

BASIC_COMMANDS = "Basic Commands"


class ControllerTypes(Enum):
    """LLM Controller Types."""

    LLAMA = "Llama"
    MARVIN = "Marvin"


@app.command(rich_help_panel=BASIC_COMMANDS)
def about():
    """About LangController."""
    print("LangController is like Django but for LLM Applications")


@Commandify(app=app, help_panel_name="Make Commands")
class MAKE:
    """Make Commands.

    Make Commands are used to scaffold new LangController Projects and
    Features
    """

    def __init__(self, template_writer: TemplateWriter):
        """Initialize MAKE with a TemplateWriter."""
        self.template_writer = template_writer

    @staticmethod
    def create_skeleton(project: Renamer):
        """Create a new LangController Project Skeleton."""
        os.mkdir(project.python_name())

        os.mkdir(f"{project.python_name()}/app")
        with open(f"{project.python_name()}/app/__init__.py", "w") as my_file:
            my_file.write(f'"""{project.human_name()} App Components."""\n')

        os.mkdir(f"{project.python_name()}/templates")
        with open(f"{project.python_name()}/templates/__init__.py", "w") as my_file:
            my_file.write(f'"""{project.human_name()} Templates."""\n')

        os.mkdir(f"{project.python_name()}/docs")
        os.mkdir(f"{project.python_name()}/docs/diagrams")

    @staticmethod
    def do_project(project_name: str):
        """Create a new LangController Project.

        Args:
            project_name (str): The name of the new LangController Project

        Example:
            langcontroller make-project scaled-agile-framework
            cd ScaledAgileFramework
        """
        if os.path.exists(project_name):
            print(f"Project {project_name} already exists")
            return

        project = Renamer(slug=project_name)
        MAKE.create_skeleton(project)

        script_path = os.path.realpath(__file__)
        script_dir = os.path.dirname(script_path)

        template_writer = TemplateWriter(template_folder=f"{script_dir}/templates")

        template_writer.render_and_write(
            template_file="top_level/create_pyproject_file.toml.j2",
            output_file=f"{project.python_name()}/pyproject.toml",
            context=dict(project_name=project.python_name()),
        )

        template_writer.render_and_write(
            template_file="top_level/create_precommit_file.yaml.j2",
            output_file=f"{project.python_name()}/.pre-commit-config.yaml",
            context=dict(),
        )

        template_writer.render_and_write(
            template_file="top_level/create_tox_file.ini.j2",
            output_file=f"{project.python_name()}/tox.ini",
            context=dict(),
        )

        template_writer.render_and_write(
            template_file="top_level/create_gitignore_file.gitignore.j2",
            output_file=f"{project.python_name()}/.gitignore",
            context=dict(),
        )

        template_writer.render_and_write(
            template_file="prompt_templates/create_prompt-base_file.j2.j2",
            output_file=f"{project.python_name()}/templates/base_prompt.j2",
            context=dict(),
        )

        template_writer.render_and_write(
            template_file="models/create_models_file.py.j2",
            output_file=f"{project.python_name()}/app/models.py",
            context=dict(project_name=project.human_name()),
        )

        template_writer.render_and_write(
            template_file="features/create_features_file.py.j2",
            output_file=f"{project.python_name()}/app/features.py",
            context=dict(project_name=project.human_name()),
        )

        template_writer.render_and_write(
            template_file="manage/create_manage_file.py.j2",
            output_file=f"{project.python_name()}/manage.py",
            context=dict(),
        )

        template_writer.render_and_write(
            template_file="pipeline/create_pipeline_file.py.j2",
            output_file=f"{project.python_name()}/app/pipeline.py",
            context=dict(project_name=project.human_name()),
        )

        template_writer.render_and_write(
            template_file="docs/interface.mermaid.j2",
            output_file=f"{project.python_name()}/docs/diagrams/interface.mermaid",
            context=dict(),
        )

        template_writer.render_and_write(
            template_file="docs/dataflow.mermaid.j2",
            output_file=f"{project.python_name()}/docs/diagrams/dataflow.mermaid",
            context=dict(),
        )

    @staticmethod
    def do_asset(
        source_action: Annotated[str, typer.Option()] = "",
        target_action: Annotated[str, typer.Option()] = "Strategy",
        target_attr_1: Annotated[str, typer.Option()] = "mission",
        target_attr_2: Annotated[str, typer.Option()] = "vision",
        target_attr_3: Annotated[str, typer.Option()] = "values",
    ):
        """Create a new LangController Feature for your LangController Project.

        Args:
            source_action (str): The name of the in coming source
            target_action (str): The name of the outgoing target
            target_attr_1 (str): The name of the first attribute
            target_attr_2 (str): The name of the second attribute
            target_attr_3 (str): The name of the third attribute

        Example:
            langcontroller make-asset --source_action strategy \
                --target_action scaled-agile-portfolio \
                --target_attr_1 name \
                --target_attr_2 description \
                --target_attr_3 issues

            python manage.py create_scaled_agile_portfolio \
                "Award-winning Tour Operator for the Moon"
        """
        if not all(
            [
                os.path.exists("app/models.py"),
                os.path.exists("app/pipeline.py"),
                os.path.exists("app/features.py"),
                os.path.exists("templates"),
                os.path.exists("manage.py"),
            ]
        ):
            print("Please verify that you are in a LangController Project")
            return

        source_action = Renamer(slug=source_action)
        target_action = Renamer(slug=target_action)
        target_attr_1 = Renamer(slug=target_attr_1)
        target_attr_2 = Renamer(slug=target_attr_2)
        target_attr_3 = Renamer(slug=target_attr_3)

        script_path = os.path.realpath(__file__)
        script_dir = os.path.dirname(script_path)
        if source_action.slug != "":
            prompt_name = f"{source_action.slug}-to-{target_action.slug}"
        else:
            prompt_name = f"{target_action.slug}"

        template_writer = TemplateWriter(template_folder=f"{script_dir}/templates")

        template_writer.render_and_write(
            template_file="models/append_marvin_class.py.j2",
            output_file="app/models.py",
            context=dict(
                target_action_human_name=target_action.human_name(),
                target_action_python_name=target_action.python_name(),
                target_attr_1_name=target_attr_1.underscore_name(),
                target_attr_2_name=target_attr_2.underscore_name(),
                target_attr_3_name=target_attr_3.underscore_name(),
            ),
            write_mode="a",
        )

        if source_action.slug != "":
            template_writer.render_and_write(
                template_file="prompt_templates/create_asset-with-source_file.j2.j2",
                output_file=f"templates/{prompt_name}.j2",
                context=dict(
                    source_action_underscore_name=source_action.underscore_name(),
                    source_action_human_name=source_action.human_name(),
                    target_action=target_action.human_name(),
                ),
            )

            template_writer.render_and_write(
                template_file="features/append_asset-with-source_class.py.j2",
                output_file="app/features.py",
                context=dict(
                    source_action_underscore_name=source_action.underscore_name(),
                    source_action_python_name=source_action.python_name(),
                    target_action_human_name=target_action.human_name(),
                    target_action_python_name=target_action.python_name(),
                    target_action_underscore_name=target_action.underscore_name(),
                    prompt_name=prompt_name,
                    controller_type=ControllerTypes.MARVIN.value,
                ),
                write_mode="a",
            )

            template_writer.render_and_write(
                template_file="pipeline/append_asset-with-source_function.py.j2",
                output_file="app/pipeline.py",
                context=dict(
                    source_action_human_name=source_action.human_name(),
                    source_action_underscore_name=source_action.underscore_name(),
                    target_action_human_name=target_action.human_name(),
                    target_action_underscore_name=target_action.underscore_name(),
                ),
                write_mode="a",
            )

        else:
            template_writer.render_and_write(
                template_file="prompt_templates/create_asset-no-source_file.j2.j2",
                output_file=f"templates/{prompt_name}.j2",
                context=dict(
                    target_action=target_action.human_name(),
                ),
            )
            template_writer.render_and_write(
                template_file="features/append_asset-no-source_class.py.j2",
                output_file="app/features.py",
                context=dict(
                    target_action_human_name=target_action.human_name(),
                    target_action_python_name=target_action.python_name(),
                    target_action_underscore_name=target_action.underscore_name(),
                    prompt_name=prompt_name,
                    controller_type=ControllerTypes.MARVIN.value,
                ),
                write_mode="a",
            )

            template_writer.render_and_write(
                template_file="pipeline/append_asset-no-source_function.py.j2",
                output_file="app/pipeline.py",
                context=dict(
                    target_action_human_name=target_action.human_name(),
                    target_action_underscore_name=target_action.underscore_name(),
                ),
                write_mode="a",
            )


if __name__ == "__main__":
    app()
