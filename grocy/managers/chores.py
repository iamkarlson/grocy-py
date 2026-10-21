from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from ..data_models.chore import Chore

if TYPE_CHECKING:
    from ..grocy_api_client import GrocyApiClient


class ChoreManager:
    """Manage household chores and their execution tracking.

    Access via ``grocy.chores``.
    """

    def __init__(self, api_client: GrocyApiClient):
        self._api = api_client

    def list(
        self, get_details: bool = False, query_filters: list[str] | None = None
    ) -> list[Chore]:
        """Get all chores.

        Args:
            get_details: Fetch full chore details for each item.
            query_filters: Optional Grocy API query filters.
        """
        raw_chores = self._api.get_chores(query_filters)
        chores = [Chore.from_current_response(chore) for chore in raw_chores]
        if get_details:
            for chore in chores:
                chore.get_details(self._api)
        return chores

    def get(self, chore_id: int) -> Chore | None:
        """Get a single chore by ID.

        Args:
            chore_id: The Grocy chore ID.
        """
        resp = self._api.get_chore(chore_id)
        return Chore.from_details_response(resp) if resp else None

    def execute(
        self,
        chore_id: int,
        done_by: int | None = None,
        tracked_time: datetime | None = None,
        skipped: bool = False,
    ):
        """Mark a chore as executed.

        Args:
            chore_id: The Grocy chore ID.
            done_by: User ID of who performed the chore.
            tracked_time: When the chore was done.
                A naive datetime is Grocy server local time; an aware datetime
                is converted to the server time zone. Defaults to the Grocy
                server clock.
            skipped: Mark as skipped rather than done.
        """
        return self._api.execute_chore(chore_id, done_by, tracked_time, skipped)

    def undo(self, execution_id: int):
        """Undo a chore execution.

        Args:
            execution_id: The chore execution ID to undo.
        """
        return self._api.undo_chore_execution(execution_id)

    def merge(self, chore_id_keep: int, chore_id_remove: int):
        """Merge two chores, keeping one and removing the other.

        Args:
            chore_id_keep: ID of the chore to keep.
            chore_id_remove: ID of the chore to remove.
        """
        return self._api.merge_chores(chore_id_keep, chore_id_remove)

    def calculate_next_assignments(self):
        """Recalculate chore assignments for all chores."""
        return self._api.calculate_chore_assignments()
