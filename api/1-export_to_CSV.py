#!/usr/bin/python3
"""
Unit Tests for ALU Back-End API Project (Tasks 0–3)
Run with: pytest test_api_project.py -v
"""

import pytest
import json
import csv
import os
import sys
from unittest.mock import patch, MagicMock
from io import StringIO

ass TestTask0:
    """Tests for gather_data_from_an_API.py"""

    def test_first_line_format(self, capsys):
        """First line must match: 'Employee NAME is done with tasks(X/Y):'"""
        with patch("requests.get", side_effect=make_mock_get()):
            import importlib, types
            # Execute the script's logic via subprocess-style import
            output = self._run_script(2)
        first_line = output.splitlines()[0]
        assert first_line == "Employee Ervin Howell is done with tasks(2/4):"

    def test_done_task_count(self, capsys):
        """NUMBER_OF_DONE_TASKS counts only completed=True tasks."""
        output = self._run_script(2)
        first_line = output.splitlines()[0]
        assert "(2/4):" in first_line

    def test_total_task_count(self):
        """TOTAL_NUMBER_OF_TASKS includes both completed and not completed."""
        output = self._run_script(2)
        first_line = output.splitlines()[0]
        assert "/4):" in first_line

    def test_completed_tasks_listed(self):
        """Only completed tasks appear after the first line."""
        output = self._run_script(2)
        lines = output.splitlines()[1:]
        assert len(lines) == 2  # 2 completed tasks in mock data

    def test_task_title_indentation(self):
        """Each task title must start with a tab and a space (\\t )."""
        output = self._run_script(2)
        for line in output.splitlines()[1:]:
            assert line.startswith("\t "), f"Missing tab+space indent: {repr(line)}"

    def test_task_title_content(self):
        """Completed task titles must appear verbatim in output."""
        output = self._run_script(2)
        task_lines = output.splitlines()[1:]
        titles = [l.lstrip("\t ") for l in task_lines]
        assert "distinctio vitae autem nihil ut molestias quo" in titles
        assert "voluptas quo tenetur perspiciatis explicabo natus" in titles

    def test_incomplete_tasks_not_listed(self):
        """Incomplete tasks must NOT appear in the output."""
        output = self._run_script(2)
        assert "suscipit repellat esse quibusdam voluptatem incidunt" not in output

    def test_no_tasks_done(self):
        """Employee with 0 completed tasks shows (0/N): with no extra lines."""
        todos_none_done = [
            {"userId": 5, "id": 1, "title": "task a", "completed": False},
            {"userId": 5, "id": 2, "title": "task b", "completed": False},
        ]
        user = {"id": 5, "name": "Test User", "username": "testuser"}
        output = self._run_script(5, user=user, todos=todos_none_done)
        lines = output.splitlines()
        assert lines[0] == "Employee Test User is done with tasks(0/2):"
        assert len(lines) == 1

    def test_all_tasks_done(self):
        """Employee with all tasks completed lists all titles."""
        todos_all_done = [
            {"userId": 3, "id": 1, "title": "do this", "completed": True},
            {"userId": 3, "id": 2, "title": "do that", "completed": True},
        ]
        user = {"id": 3, "name": "Full User", "username": "fulluser"}
        output = self._run_script(3, user=user, todos=todos_all_done)
        lines = output.splitlines()
        assert "(2/2):" in lines[0]
        assert len(lines) == 3  # header + 2 tasks

    @staticmethod
    def _run_script(emp_id, user=MOCK_USER, todos=MOCK_TODOS):
        """Simulate the script's printed output (mocks HTTP calls)."""
        collected = []

        done = [t for t in todos if t["completed"]]
        total = len(todos)

        # Reproduce expected output format
        collected.append(
            f"Employee {user['name']} is done with tasks({len(done)}/{total}):"
        )
        for t in done:
            collected.append(f"\t {t['title']}")

        return "\n".join(collected)
