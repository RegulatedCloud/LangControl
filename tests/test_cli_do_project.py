import os
import unittest
import tempfile
from unittest.mock import patch
from langcontroller.cli import TemplateWriter, MAKE


class CLIMakeTestCase(unittest.TestCase):
    def setUp(self):
        script_path = os.path.realpath(__file__)
        self.script_dir = os.path.dirname(script_path)
        self.template_folder = f"{self.script_dir}/../langcontroller/templates"
        self.template_writer = TemplateWriter(template_folder=self.template_folder)
        self.obj = MAKE(self.template_writer)

    def test_do_project(self):
        with patch("os.mkdir") as mock_mkdir, patch("builtins.open"), patch(
            "langcontroller.cli.TemplateWriter.render_and_write"
        ) as mock_render_and_write:
            temp_folder = tempfile.TemporaryDirectory(
                prefix="TestProject", dir=f"{self.script_dir}/../"
            )
            project_name = temp_folder.name.split("/")[-1]
            self.obj.do_project(project_name=project_name)

            mock_mkdir.assert_called()
            mock_render_and_write.assert_called()

    def test_template_file_exists(self):
        with patch("os.mkdir"), patch("builtins.open"), patch(
            "langcontroller.cli.TemplateWriter.render_and_write"
        ) as mock_render_and_write:
            mock_render_and_write.return_value = None

            temp_folder = tempfile.TemporaryDirectory(
                prefix="TestProject", dir=f"{self.script_dir}/../"
            )
            project_name = temp_folder.name.split("/")[-1]
            self.obj.do_project(project_name=project_name)

            mock_render_and_write.assert_called()

            _, args = mock_render_and_write.call_args
            template_file = args["template_file"]
            template_file_path = os.path.join(self.template_folder, template_file)

            self.assertTrue(
                os.path.exists(template_file_path),
                f"Template file {template_file_path} does not exist",
            )


if __name__ == "__main__":
    unittest.main()
