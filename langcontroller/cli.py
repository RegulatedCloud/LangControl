"""A Generative AI Python Application Framework inspired by Django, Laravel, and Meltano

Features:
    Architected for both Human and AI Devs
    Scaffolds are designed to help your AI Code Assistant
    Generated components render with CLI, FastAPI, and Dagster

Template Naming Conventions:
    <domain>_<operation>_<data_type>
    domain - manage|models|pipeline|prompt_templates|pyproject|repository
    operation - append|create
    data_type - asset|class|function|file|prompt|sensor

"""
import os

from rich import print
from jinja2 import Environment, FileSystemLoader, select_autoescape

import typer
from slugify import slugify

app = typer.Typer(rich_markup_mode="rich")

BASIC_COMMANDS = "Basic Commands"


class Renamer:
    """Rename a string to a slug, python name, or human name"""

    def __init__(self, slug: str):
        """Initialize Renamer with a slug"""
        self.slug = slugify(slug)

    def human_name(self):
        """Return a human name from a slug

        Example:
            scaled-agile-framework -> Scaled Agile Framework
        """
        return self.slug.replace('-', ' ').title()

    def python_name(self):
        """Return a python name from a slug

        Example:
            scaled-agile-framework -> ScaledAgileFramework
        """
        return self.human_name().replace(' ', '')

    def underscore_name(self):
        """Return an underscore name from a slug

        Example:
            scaled-agile-framework -> scaled_agile_framework
        """
        return self.slug.replace('-', '_')


class Commandify:
    """Decorator to convert a class into a typer command"""

    def __init__(self, help_panel_name: str):
        """Initialize Commandify with a help panel name

        Args:
            help_panel_name (str): The name of the typer help panel
        """
        self.help_panel_name = help_panel_name

    def __call__(self, cls):
        """Convert methods in a class into a typer repository

        Setup Steps:
            1. Decorate class with Commandify
            2. Decorate class methods with @staticmethod

        Commandify Steps:
            1. Find all class methods that start with "do_"
            2. Convert the class method name to a slug
            3. Decorate the class method with "app.command"

        Args:
            cls (class): The class to decorate class methods into a typer repository
        """
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
    """Make Commands

    Make Commands are used to scaffold new LangController Projects and Features
    """

    @staticmethod
    def do_project(project_name: str):
        """Create a new LangController Project

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
        os.mkdir(project.python_name())
        os.mkdir(f"{project.python_name()}/app")
        f = open(f"{project.python_name()}/app/__init__.py", "w")
        f.close()
        os.mkdir(f"{project.python_name()}/templates")
        f = open(f"{project.python_name()}/templates/__init__.py", "w")
        f.close()

        script_path = os.path.realpath(__file__)
        script_dir = os.path.dirname(script_path)

        env = Environment(
            loader=FileSystemLoader(f"{script_dir}/templates"),
            autoescape=select_autoescape(),
        )
        template = env.get_template("pyproject/create_pyproject_file.toml.j2")
        file_contents = template.render(dict(
            project_name=project.python_name()
        ))
        with open(f"{project.python_name()}/pyproject.toml", "w") as f:
            f.write(file_contents)

        template = env.get_template("prompt_templates/create_prompt-base_file.j2.j2")
        file_contents = template.render()
        with open(f"{project.python_name()}/templates/base_prompt.j2", "w") as f:
            f.write(file_contents)

        template = env.get_template("models/create_models_file.py.j2")
        file_contents = template.render(
            project_name=project.human_name()
        )
        with open(f"{project.python_name()}/app/models.py", "w") as f:
            f.write(file_contents)

        template = env.get_template("repository/create_repository_file.py.j2")
        file_contents = template.render(
            project_name=project.human_name()
        )
        with open(f"{project.python_name()}/app/repository.py", "w") as f:
            f.write(file_contents)

        template = env.get_template("manage/create_manage_file.py.j2")
        file_contents = template.render()
        with open(f"{project.python_name()}/manage.py", "w") as f:
            f.write(file_contents)

        template = env.get_template("pipeline/create_pipeline_file.py.j2")
        file_contents = template.render(dict(
            project_name=project.human_name()
        ))
        with open(f"{project.python_name()}/app/pipeline.py", "w") as f:
            f.write(file_contents)

    @staticmethod
    def do_sensor(target_action: str, attribute_1: str, attribute_2: str, attribute_3: str):
        """Create a new LangController Feature from inside your LangController Project

        Args:
            target_action (str): The name of the outgoing target
            attribute_1 (str): The name of the first attribute of the target action
            attribute_2 (str): The name of the second attribute of the target action
            attribute_3 (str): The name of the third attribute of the target action

        Example:
            langcontroller make-sensor strategy mission vision values
            python manage.py create_strategy "Tour Operator for the Moon"
        """

        if not all([
            os.path.exists("app/models.py"),
            os.path.exists("app/pipeline.py"),
            os.path.exists("app/repository.py"),
            os.path.exists("manage.py"),
            os.path.exists("templates"),
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

        template = env.get_template("prompt_templates/create_sensor_file.j2.j2")
        my_prompt = template.render(dict(
            target_action=target_action.human_name(),
        ))
        with open(f"templates/{prompt_name}.j2", "w") as f:
            f.write(my_prompt)

        template = env.get_template("models/append_marvin_class.py.j2")
        my_model = template.render(dict(
            target_action_human_name=target_action.human_name(),
            target_action_python_name=target_action.python_name(),
            attribute_1_name=attribute_1.underscore_name(),
            attribute_2_name=attribute_2.underscore_name(),
            attribute_3_name=attribute_3.underscore_name(),
        ))
        with open("app/models.py", "a") as f:
            f.write("\n\n")
            f.write(my_model)

        template = env.get_template("repository/append_sensor_class.py.j2")
        my_function = template.render(dict(
            target_action_human_name=target_action.human_name(),
            target_action_python_name=target_action.python_name(),
            target_action_underscore_name=target_action.underscore_name(),
            prompt_name=prompt_name,
            controller_type="Marvin",
        ))
        with open("app/repository.py", "a") as f:
            f.write("\n\n")
            f.write(my_function)

        template = env.get_template("pipeline/append_sensor_function.py.j2")
        my_asset = template.render(dict(
            target_action_human_name=target_action.human_name(),
            target_action_underscore_name=target_action.underscore_name(),
        ))
        with open("app/pipeline.py", "a") as f:
            f.write("\n\n")
            f.write(my_asset)

    @staticmethod
    def do_asset(source_action: str, target_action: str,
                 attribute_1: str, attribute_2: str, attribute_3: str):
        """Create a new LangController Feature from inside your LangController Project

        Args:
            source_action (str): The name of the in coming source
            target_action (str): The name of the outgoing target
            attribute_1 (str): The name of the first attribute of the target action
            attribute_2 (str): The name of the second attribute of the target action
            attribute_3 (str): The name of the third attribute of the target action

        Example:
            langcontroller make-asset strategy scaled-agile-portfolio name description issues
            python manage.py create_scaled_agile_portfolio "Award-winning Tour Operator for the Moon"
        """

        if not all([
            os.path.exists("app/models.py"),
            os.path.exists("app/pipeline.py"),
            os.path.exists("app/repository.py"),
            os.path.exists("templates"),
            os.path.exists("manage.py"),
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

        template = env.get_template("prompt_templates/create_asset_file.j2.j2")
        my_prompt = template.render(dict(
            source_action_underscore_name=source_action.underscore_name(),
            source_action_human_name=source_action.human_name(),
            target_action=target_action.human_name()
        ))
        with open(f"templates/{prompt_name}.j2", "w") as f:
            f.write(my_prompt)

        template = env.get_template("models/append_marvin_class.py.j2")
        my_model = template.render(dict(
            target_action_human_name=target_action.human_name(),
            target_action_python_name=target_action.python_name(),
            attribute_1_name=attribute_1.underscore_name(),
            attribute_2_name=attribute_2.underscore_name(),
            attribute_3_name=attribute_3.underscore_name(),
        ))
        with open("app/models.py", "a") as f:
            f.write("\n\n")
            f.write(my_model)

        template = env.get_template("repository/append_asset_class.py.j2")
        my_function = template.render(dict(
            source_action_underscore_name=source_action.underscore_name(),
            target_action_human_name=target_action.human_name(),
            target_action_python_name=target_action.python_name(),
            target_action_underscore_name=target_action.underscore_name(),
            prompt_name=prompt_name,
            controller_type="Marvin",
        ))
        with open("app/repository.py", "a") as f:
            f.write("\n\n")
            f.write(my_function)

        template = env.get_template("pipeline/append_asset_function.py.j2")
        my_asset = template.render(dict(
            source_action_human_name=source_action.human_name(),
            source_action_underscore_name=source_action.underscore_name(),
            target_action_human_name=target_action.human_name(),
            target_action_underscore_name=target_action.underscore_name(),
        ))
        with open("app/pipeline.py", "a") as f:
            f.write("\n\n")
            f.write(my_asset)


if __name__ == "__main__":
    app()
