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

    @patch("argparse.ArgumentParser.parse_args")
    @patch("relm.main.find_projects")
    @patch("relm.main.run_project_command")
    @patch("relm.main.console")
    def test_main_run_all(self, mock_console, mock_run_cmd, mock_find_projects, mock_parse_args):
        mock_parse_args.return_value = MagicMock(
            command="run",
            path=".",
            command_string="echo test",
            project_name="all",
            fail_fast=False
        )
        p1 = Project("proj1", "1.0.0", Path("."), "desc")
        p2 = Project("proj2", "1.0.0", Path("."), "desc")
        mock_find_projects.return_value = [p1, p2]
        mock_run_cmd.side_effect = [True, False]

        with self.assertRaises(SystemExit):
            # Because one failed, it exits with 1 at the end
            main()

        self.assertEqual(mock_run_cmd.call_count, 2)
        mock_console.rule.assert_called_with("Execution Summary")

    @patch("argparse.ArgumentParser.parse_args")
    @patch("relm.main.find_projects")
    @patch("relm.main.run_project_command")
    @patch("relm.main.console")
    def test_main_run_fail_fast(self, mock_console, mock_run_cmd, mock_find_projects, mock_parse_args):
        mock_parse_args.return_value = MagicMock(
            command="run",
            path=".",
            command_string="echo test",
            project_name="all",
            fail_fast=True
        )
        p1 = Project("proj1", "1.0.0", Path("."), "desc")
        p2 = Project("proj2", "1.0.0", Path("."), "desc")
        mock_find_projects.return_value = [p1, p2]
        mock_run_cmd.side_effect = [False, True] # First fails

        with self.assertRaises(SystemExit):
            main()

        self.assertEqual(mock_run_cmd.call_count, 1)

    @patch("argparse.ArgumentParser.parse_args")
    @patch("relm.main.find_projects")
    @patch("relm.main.run_project_command")
    @patch("relm.main.console")
    def test_main_run_single_success(self, mock_console, mock_run_cmd, mock_find_projects, mock_parse_args):
        mock_parse_args.return_value = MagicMock(
            command="run",
            path=".",
            command_string="echo test",
            project_name="proj1",
            fail_fast=False
        )
        p1 = Project("proj1", "1.0.0", Path("."), "desc")
        mock_find_projects.return_value = [p1]
        mock_run_cmd.return_value = True

        main()

        mock_run_cmd.assert_called_once()
        mock_console.print.assert_any_call("[green]Success: 1[/green] ['proj1']")

    @patch("argparse.ArgumentParser.parse_args")
    @patch("relm.main.find_projects")
    @patch("relm.main.console")
    def test_main_run_project_not_found(self, mock_console, mock_find_projects, mock_parse_args):
        mock_parse_args.return_value = MagicMock(
            command="run",
            path=".",
            command_string="echo test",
            project_name="nonexistent",
            fail_fast=False
        )
        mock_find_projects.return_value = []

        with self.assertRaises(SystemExit):
            main()

        # The path is resolved to absolute path in main.py, so we need to match that
        root_path = Path(".").resolve()
        mock_console.print.assert_any_call(f"[red]Project 'nonexistent' not found in {root_path}[/red]")

    @patch("argparse.ArgumentParser.parse_args")
    @patch("relm.main.find_projects")
    @patch("relm.main.install_project")
    @patch("relm.main.console")
    def test_main_install_all(self, mock_console, mock_install, mock_find_projects, mock_parse_args):
        mock_parse_args.return_value = MagicMock(
            command="install",
            path=".",
            project_name="all",
            no_editable=False
        )
        p1 = Project("proj1", "1.0.0", Path("."), "desc")
        p2 = Project("proj2", "1.0.0", Path("."), "desc")
        mock_find_projects.return_value = [p1, p2]
        mock_install.side_effect = [True, False]

        main()

        self.assertEqual(mock_install.call_count, 2)
        mock_console.rule.assert_called_with("Bulk Install Summary")

    @patch("argparse.ArgumentParser.parse_args")
    @patch("relm.main.find_projects")
    @patch("relm.main.install_project")
    @patch("relm.main.console")
    def test_main_install_single_success(self, mock_console, mock_install, mock_find_projects, mock_parse_args):
        mock_parse_args.return_value = MagicMock(
            command="install",
            path=".",
            project_name="proj1",
            no_editable=False
        )
        p1 = Project("proj1", "1.0.0", Path("."), "desc")
        mock_find_projects.return_value = [p1]
        mock_install.return_value = True

        main()

        mock_install.assert_called_once()

    @patch("argparse.ArgumentParser.parse_args")
    @patch("relm.main.find_projects")
    @patch("relm.main.console")
    def test_main_install_project_not_found(self, mock_console, mock_find_projects, mock_parse_args):
        mock_parse_args.return_value = MagicMock(
            command="install",
            path=".",
            project_name="nonexistent",
            no_editable=False
        )
        mock_find_projects.return_value = []

        with self.assertRaises(SystemExit):
            main()

        root_path = Path(".").resolve()
        mock_console.print.assert_any_call(f"[red]Project 'nonexistent' not found in {root_path}[/red]")

    @patch("argparse.ArgumentParser.parse_args")
    @patch("relm.main.find_projects")
    @patch("relm.main.get_current_branch")
    @patch("relm.main.is_git_clean")
    @patch("relm.main.console")
    def test_main_status_all(self, mock_console, mock_is_clean, mock_get_branch, mock_find_projects, mock_parse_args):
        mock_parse_args.return_value = MagicMock(
            command="status",
            path=".",
            project_name="all"
        )
        p1 = Project("proj1", "1.0.0", Path("."), "desc")
        mock_find_projects.return_value = [p1]
        mock_get_branch.return_value = "main"
        mock_is_clean.return_value = True

        main()

        mock_console.print.assert_called()
        args, _ = mock_console.print.call_args
        self.assertTrue(hasattr(args[0], "rows"))

    @patch("argparse.ArgumentParser.parse_args")
    @patch("relm.main.find_projects")
    @patch("relm.main.get_current_branch")
    @patch("relm.main.is_git_clean")
    @patch("relm.main.console")
    def test_main_status_single(self, mock_console, mock_is_clean, mock_get_branch, mock_find_projects, mock_parse_args):
        mock_parse_args.return_value = MagicMock(
            command="status",
            path=".",
            project_name="proj1"
        )
        p1 = Project("proj1", "1.0.0", Path("."), "desc")
        mock_find_projects.return_value = [p1]
        mock_get_branch.return_value = "main"
        mock_is_clean.return_value = False

        main()

        mock_console.print.assert_called()

    @patch("argparse.ArgumentParser.parse_args")
    @patch("relm.main.find_projects")
    @patch("relm.main.console")
    def test_main_status_project_not_found(self, mock_console, mock_find_projects, mock_parse_args):
        mock_parse_args.return_value = MagicMock(
            command="status",
            path=".",
            project_name="nonexistent"
        )
        mock_find_projects.return_value = []

        with self.assertRaises(SystemExit):
            main()

        root_path = Path(".").resolve()
        mock_console.print.assert_any_call(f"[red]Project 'nonexistent' not found in {root_path}[/red]")

    @patch("argparse.ArgumentParser.parse_args")
    @patch("relm.main.console")
    def test_main_safety_check(self, mock_console, mock_parse_args):
        # Determine the root path of the system
        root_path = Path.cwd().root

        mock_parse_args.return_value = MagicMock(
            command="list",
            path=str(root_path),
            yes=False
        )

        # Simulate user saying "n" to the prompt
        mock_console.input.return_value = "n"

        with self.assertRaises(SystemExit):
            main()

        mock_console.print.assert_any_call(f"[bold red]⚠️  Safety Warning: You are running relm in the system root ({root_path}).[/bold red]")

    @patch("argparse.ArgumentParser.parse_args")
    @patch("relm.main.list_projects")
    @patch("relm.main.console")
    def test_main_safety_check_yes(self, mock_console, mock_list_projects, mock_parse_args):
        # Determine the root path of the system
        root_path = Path.cwd().root

        mock_parse_args.return_value = MagicMock(
            command="list",
            path=str(root_path),
            yes=True
        )

        main()

        mock_list_projects.assert_called()

if __name__ == "__main__":
    unittest.main()
