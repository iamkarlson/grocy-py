from __future__ import annotations

from typing import TYPE_CHECKING

from ..data_models.chore_log import ChoreLog

if TYPE_CHECKING:
    from ..grocy_api_client import GrocyApiClient


class ChoreLogManager:
    """Manage household chores logs.

    Access via ``grocy.chores_log``.
    """

    def __init__(self, api_client: GrocyApiClient):
        self._api = api_client

    def list(
        self, get_details: bool = False, query_filters: list[str] | None = None
    ) -> list[ChoreLog]:
        """Get all chores log.

        Args:
            get_details: Fetch full chore log details for each item.
            query_filters: Optional Grocy API query filters.
        """
        raw_chores_log = self._api.get_chores_log(query_filters)
        chores_log = [ChoreLog.from_response(chore_log) for chore_log in raw_chores_log]
        if get_details:
            for chore_log in chores_log:
                chore_log.get_details(self._api)
        return chores_log

    def get(self, chore_log_id: int) -> ChoreLog:
        """Get a single chore log by ID.

        Args:
            chore_log_id: The Grocy chore log ID.
        """
        resp = self._api.get_chore_log(chore_log_id)
        return ChoreLog.from_response(resp)

    # def undo(self, execution_id: int):
    #     """Undo a chore log execution.

    #     Args:
    #         execution_id: The chore log execution ID to undo.
    #     """
    #     return self._api.undo_chore_log_execution(execution_id)

