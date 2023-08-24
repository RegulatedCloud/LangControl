"""Utility functions for LangController."""
from typing import Dict

import typer
from rich import print
from jinja2 import Environment, FileSystemLoader, select_autoescape

from slugify import slugify


class Renamer:
    """Rename a string to a slug, python name, or human name."""

    def __init__(self, slug: str):
        """Initialize Renamer with a slug."""
        self.slug = slugify(slug)

    def human_name(self):
        """Return a human name from a slug.

        Example:
            scaled-agile-framework -> Scaled Agile Framework
        """
        return self.slug.replace("-", " ").title()

    def python_name(self):
        """Return a python name from a slug.

        Example:
            scaled-agile-framework -> ScaledAgileFramework
        """
        return self.human_name().replace(" ", "")

    def underscore_name(self):
        """Return an underscore name from a slug.

        Example:
            scaled-agile-framework -> scaled_agile_framework
        """
        return self.slug.replace("-", "_")


class Commandify:
    """Decorator to convert a class into a typer command."""

    def __init__(self, app: typer.Typer, help_panel_name: str):
        """Initialize Commandify with a help panel name.

        Args:
            app (typer.Typer): The typer app to add commands to
            help_panel_name (str): The name of the typer help panel
        """
        self.app = app
        self.help_panel_name = help_panel_name

    def __call__(self, cls):
        """Convert methods in a class into a typer repository.

        Setup Steps:
            1. Decorate class with Commandify
            2. Decorate class methods with @staticmethod

        Commandify Steps:
            1. Find all class methods that start with "do_"
            2. Convert the class method name to a slug
            3. Decorate the class method with "app.command"

        Args:
            cls (class): The class to add decorators to
        """
        for attr_name, attr_value in vars(cls).items():
            if callable(attr_value) and attr_name.startswith("do_"):
                cls_name = cls.__name__.lower()
                attribute_name = slugify(attr_name[3:])
                new_name = f"{cls_name}-{attribute_name}"
                new_command = self.app.command(
                    name=new_name, rich_help_panel=self.help_panel_name
                )
                setattr(cls, attr_name, new_command(attr_value))
        return cls


class TemplateWriter:
    """Renders Jinja2 templates and writes them to files."""

    def __init__(self, template_folder: str):
        """Initialize TemplateWriter with a template folder."""
        self.env = Environment(
            loader=FileSystemLoader(template_folder),
            autoescape=select_autoescape(),
        )

    def render_and_write(
        self,
        template_file: str,
        output_file: str,
        context: Dict[str, str],
        write_mode="w",
    ) -> None:
        """Renders a Jinja2 template and writes it to an output file.

        Args:
            template_file (str): The name of the template file
            output_file (str): The name of the output file
            context (Dict[str, str]): The context to render the template with
            write_mode (str): The write mode to use when writing to the file
        """
        try:
            template = self.env.get_template(template_file)
        except Exception as e:
            print(f"Error loading template: {e}")
            return

        try:
            file_contents = template.render(context)
        except Exception as e:
            print(f"Error rendering template: {e}")
            return

        try:
            with open(output_file, write_mode) as my_file:
                if write_mode == "a":
                    my_file.write("\n\n")
                my_file.write(file_contents)
        except Exception as e:
            print(f"Error writing to output file: {e}")
