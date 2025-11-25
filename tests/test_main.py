# tests/test_main.py

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys
from relm.main import main, list_projects
from relm.core import Project

class TestMain(unittest.TestCase):
    @patch("relm.main.find_projects")
    @patch("relm.main.console")
    def test_list_projects(self, mock_console, mock_find_projects):
        mock_find_projects.return_value = [
            Project("proj1", "1.0.0", Path("path/to/proj1"), "desc1"),
            Project("proj2", "2.0.0", Path("path/to/proj2"), None)
        ]

        list_projects(Path("."))

        mock_console.print.assert_called()
        args, _ = mock_console.print.call_args
        self.assertTrue(hasattr(args[0], "rows")) # It's a Table object

    @patch("relm.main.find_projects")
    @patch("relm.main.console")
    def test_list_projects_empty(self, mock_console, mock_find_projects):
        mock_find_projects.return_value = []
        list_projects(Path("."))
        mock_console.print.assert_called_with("[yellow]No projects found in this directory.[/yellow]")

    @patch("argparse.ArgumentParser.parse_args")
    @patch("relm.main.list_projects")
    def test_main_list(self, mock_list_projects, mock_parse_args):
        mock_parse_args.return_value = MagicMock(command="list", path=".")
        main()
        mock_list_projects.assert_called()

    @patch("argparse.ArgumentParser.parse_args")
    @patch("relm.main.find_projects")
    @patch("relm.main.perform_release")
    @patch("relm.main.console")
    def test_main_release_single_success(self, mock_console, mock_perform_release, mock_find_projects, mock_parse_args):
        mock_parse_args.return_value = MagicMock(
            command="release",
            path=".",
            project_name="proj1",
            type="patch",
            yes=True
        )
        project = Project("proj1", "1.0.0", Path("."), "desc")
        mock_find_projects.return_value = [project]
        mock_perform_release.return_value = True

        main()

        mock_perform_release.assert_called_with(project, "patch", yes_mode=True, check_changes=False)

    @patch("argparse.ArgumentParser.parse_args")
    @patch("relm.main.find_projects")
    @patch("relm.main.console")
    def test_main_release_project_not_found(self, mock_console, mock_find_projects, mock_parse_args):
        mock_parse_args.return_value = MagicMock(
            command="release",
            path=".",
            project_name="nonexistent",
            type="patch",
            yes=True
        )
        mock_find_projects.return_value = []

        with self.assertRaises(SystemExit):
            main()

        mock_console.print.assert_called()

    @patch("argparse.ArgumentParser.parse_args")
    @patch("relm.main.find_projects")
    @patch("relm.main.perform_release")
    @patch("relm.main.console")
    def test_main_release_all(self, mock_console, mock_perform_release, mock_find_projects, mock_parse_args):
        mock_parse_args.return_value = MagicMock(
            command="release",
            path=".",
            project_name="all",
            type="patch",
            yes=True
        )
        p1 = Project("proj1", "1.0.0", Path("."), "desc")
        p2 = Project("proj2", "1.0.0", Path("."), "desc")
        mock_find_projects.return_value = [p1, p2]
        mock_perform_release.side_effect = [True, False] # One released, one skipped

        main()

        self.assertEqual(mock_perform_release.call_count, 2)
        # Verify summary printed
        mock_console.rule.assert_called_with("Bulk Release Summary")

    @patch("argparse.ArgumentParser.parse_args")
    @patch("relm.main.find_projects")
    @patch("relm.main.perform_release")
    @patch("relm.main.console")
    def test_main_release_all_exception(self, mock_console, mock_perform_release, mock_find_projects, mock_parse_args):
        mock_parse_args.return_value = MagicMock(
            command="release",
            path=".",
            project_name="all",
            type="patch",
            yes=True
        )
        p1 = Project("proj1", "1.0.0", Path("."), "desc")
        mock_find_projects.return_value = [p1]
        mock_perform_release.side_effect = Exception("Boom")

        main()

        mock_console.print.assert_any_call("[red]Critical error releasing proj1: Boom[/red]")

if __name__ == "__main__":
    unittest.main()
