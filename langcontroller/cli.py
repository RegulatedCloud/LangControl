"""
A Generative AI Application Framework inspired by Django, Laravel, and Meltano

Features
    Comments to help your LLM Code Assistant
    Structures and Comments to help both Human and AI Devs

TODO Write Doc Strings for AI

TODO FastAPI
TODO manage.py runs the FastAPI Server and maybe the CLI

TODO BasePrompt feature
TODO Middleware
TODO Tests
"""
import os

from rich import print
from jinja2 import Environment, FileSystemLoader, select_autoescape

import typer
from slugify import slugify

app = typer.Typer(rich_markup_mode="rich")

BASIC_COMMANDS = "Basic Commands"


class Renamer:
    def __init__(self, slug: str):
        self.slug = slugify(slug)

    def human_name(self):
        return self.slug.replace('-', ' ').title()

    def python_name(self):
        return self.human_name().replace(' ', '')

    def underscore_name(self):
        return self.slug.replace('-', '_')


class Commandify:
    def __init__(self, help_panel_name: str):
        self.help_panel_name = help_panel_name

    def __call__(self, cls):
        for attr_name, attr_value in vars(cls).items():
            if callable(attr_value) and attr_name.startswith("do_"):
                cls_name = cls.__name__.lower()
                attribute_name = slugify(attr_name[3:])
                new_name = f"{cls_name}-{attribute_name}"
                new_command = app.command(
                    name=new_name,
                    rich_help_panel=self.help_panel_name
                )
                setattr(cls, attr_name, new_command(attr_value))
        return cls


@app.command(rich_help_panel=BASIC_COMMANDS)
def about():
    """About LangController"""
    print("LangController is like Django but for LLM Applications")


@Commandify(help_panel_name='Make Commands')
class MAKE:
    @staticmethod
    def do_project(project_name: str):
        """Create a new LangController Project

        langcontroller make-project scaled-agile-framework
        cd ScaledAgileFramework
        """
        if os.path.exists(project_name):
            print(f"Project {project_name} already exists")
            return

        project = Renamer(slug=project_name)
        os.mkdir(project.python_name())
        os.mkdir(f"{project.python_name()}/prompt_templates")
        f = open(f"{project.python_name()}/prompt_templates/__init__.py", "w")
        f.close()

        script_path = os.path.realpath(__file__)
        script_dir = os.path.dirname(script_path)

        env = Environment(
            loader=FileSystemLoader(f"{script_dir}/templates"),
            autoescape=select_autoescape(),
        )
        template = env.get_template("pyproject_file.toml.jinja2")
        file_contents = template.render(dict(
            project_name=project.python_name()
        ))
        with open(f"{project.python_name()}/pyproject.toml", "w") as f:
            f.write(file_contents)

        template = env.get_template("models_file.jinja2")
        file_contents = template.render()
        with open(f"{project.python_name()}/models.py", "w") as f:
            f.write(file_contents)

        template = env.get_template("command_file.jinja2")
        file_contents = template.render()
        with open(f"{project.python_name()}/commands.py", "w") as f:
            f.write(file_contents)

        template = env.get_template("cli_file.jinja2")
        file_contents = template.render()
        with open(f"{project.python_name()}/cli.py", "w") as f:
            f.write(file_contents)

        template = env.get_template("pipeline_file.jinja2")
        file_contents = template.render(dict(
            project_name=project.human_name()
        ))
        with open(f"{project.python_name()}/pipeline.py", "w") as f:
            f.write(file_contents)

    @staticmethod
    def do_feature_no_source(target_action: str, attribute_1: str, attribute_2: str, attribute_3: str):
        """Create a new LangController Feature inside your LangController Project

        Example:
            langcontroller make-feature-no-input strategy mission vision values
            poetry run python commands.py create_strategy "Tour Operator for the Moon"
        """

        if not all([
            os.path.exists("commands.py"),
            os.path.exists("pipeline.py"),
            os.path.exists("prompt_templates"),
        ]):
            print("Please verify that you are in a LangController Project")
            return

        target_action = Renamer(slug=target_action)
        attribute_1 = Renamer(slug=attribute_1)
        attribute_2 = Renamer(slug=attribute_2)
        attribute_3 = Renamer(slug=attribute_3)

        script_path = os.path.realpath(__file__)
        script_dir = os.path.dirname(script_path)

        env = Environment(
            loader=FileSystemLoader(f"{script_dir}/templates"),
            autoescape=select_autoescape(),
        )
        prompt_name = f"{target_action.slug}"

        template = env.get_template("prompt_command_no_source.jinja2")
        my_prompt = template.render(dict(
            target_action=target_action.human_name(),
        ))
        with open(f"prompt_templates/{prompt_name}.jinja2", "w") as f:
            f.write(my_prompt)

        template = env.get_template("models_class.jinja2")
        my_model = template.render(dict(
            target_action_human_name=target_action.human_name(),
            target_action_python_name=target_action.python_name(),
            attribute_1_name=attribute_1.underscore_name(),
            attribute_2_name=attribute_2.underscore_name(),
            attribute_3_name=attribute_3.underscore_name(),
        ))
        with open("models.py", "a") as f:
            f.write("\n\n")
            f.write(my_model)

        template = env.get_template("command_function_no_source.jinja2")
        my_function = template.render(dict(
            target_action_human_name=target_action.human_name(),
            target_action_python_name=target_action.python_name(),
            target_action_underscore_name=target_action.underscore_name(),
            prompt_name=prompt_name,
            controller_type="Marvin",
        ))
        with open("commands.py", "a") as f:
            f.write("\n\n")
            f.write(my_function)

        template = env.get_template("pipeline_function_no_source.jinja2")
        my_asset = template.render(dict(
            target_action_human_name=target_action.human_name(),
            target_action_underscore_name=target_action.underscore_name(),
        ))
        with open("pipeline.py", "a") as f:
            f.write("\n\n")
            f.write(my_asset)

    @staticmethod
    def do_feature_with_source(source_action: str, target_action: str, attribute_1: str, attribute_2: str,
                               attribute_3: str):
        """Create a new LangController Feature inside your LangController Project

        Example:
            langcontroller make-feature strategy scaled-agile-portfolio name description issues
            poetry run python commands.py create_scaled_agile_portfolio --strategy "Tour Operator for the Moon"
        """

        if not all([
            os.path.exists("commands.py"),
            os.path.exists("pipeline.py"),
            os.path.exists("prompt_templates"),
        ]):
            print("Please verify that you are in a LangController Project")
            return

        source_action = Renamer(slug=source_action)
        target_action = Renamer(slug=target_action)
        attribute_1 = Renamer(slug=attribute_1)
        attribute_2 = Renamer(slug=attribute_2)
        attribute_3 = Renamer(slug=attribute_3)

        script_path = os.path.realpath(__file__)
        script_dir = os.path.dirname(script_path)

        env = Environment(
            loader=FileSystemLoader(f"{script_dir}/templates"),
            autoescape=select_autoescape(),
        )
        prompt_name = f"{source_action.slug}-to-{target_action.slug}"

        template = env.get_template("prompt_command_with_source.jinja2")
        my_prompt = template.render(dict(
            target_action=target_action.human_name(),
            source_action=source_action.human_name()
        ))
        with open(f"prompt_templates/{prompt_name}.jinja2", "w") as f:
            f.write("\n\n")
            f.write(my_prompt)

        template = env.get_template("models_class.jinja2")
        my_model = template.render(dict(
            target_action_human_name=target_action.human_name(),
            target_action_python_name=target_action.python_name(),
            attribute_1_name=attribute_1.underscore_name(),
            attribute_2_name=attribute_2.underscore_name(),
            attribute_3_name=attribute_3.underscore_name(),
        ))
        with open("models.py", "a") as f:
            f.write("\n\n")
            f.write(my_model)

        template = env.get_template("command_function_with_source.jinja2")
        my_function = template.render(dict(
            source_action_underscore_name=source_action.underscore_name(),
            target_action_human_name=target_action.human_name(),
            target_action_python_name=target_action.python_name(),
            target_action_underscore_name=target_action.underscore_name(),
            prompt_name=prompt_name,
            controller_type="Marvin",
        ))
        with open("commands.py", "a") as f:
            f.write("\n\n")
            f.write(my_function)

        template = env.get_template("pipeline_function_with_source.jinja2")
        my_asset = template.render(dict(
            source_action_human_name=source_action.human_name(),
            source_action_underscore_name=source_action.underscore_name(),
            target_action_human_name=target_action.human_name(),
            target_action_underscore_name=target_action.underscore_name(),
        ))
        with open("pipeline.py", "a") as f:
            f.write("\n\n")
            f.write(my_asset)


if __name__ == "__main__":
    app()
