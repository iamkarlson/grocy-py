from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from ..data_models.task import Task

if TYPE_CHECKING:
    from ..grocy_api_client import GrocyApiClient


class TaskManager:
    """Manage tasks and their completion status.

    Access via ``grocy.tasks``.
    """

    def __init__(self, api_client: GrocyApiClient):
        self._api = api_client

    def list(self, query_filters: list[str] | None = None) -> list[Task]:
        """Get all tasks."""
        raw_tasks = self._api.get_tasks(query_filters)
        return [Task.from_response(task) for task in raw_tasks]

    def get(self, task_id: int) -> Task | None:
        """Get a single task by ID.

        Args:
            task_id: The Grocy task ID.
        """
        resp = self._api.get_task(task_id)
        return Task.from_response(resp) if resp else None

    def complete(self, task_id: int, done_time: datetime | None = None):
        """Mark a task as completed.

        Args:
            task_id: The Grocy task ID.
            done_time: When the task was completed.
                A naive datetime is Grocy server local time; an aware datetime
                is converted to the server time zone. Defaults to the Grocy
                server clock.
        """
        return self._api.complete_task(task_id, done_time)

    def undo(self, task_id: int):
        """Undo a task completion.

        Args:
            task_id: The Grocy task ID.
        """
        return self._api.undo_task(task_id)
