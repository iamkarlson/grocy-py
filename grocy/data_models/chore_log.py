from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from .user import User
from .chore import Chore
from ..grocy_api_client import GrocyApiClient



class ChoreLog(BaseModel):
    """A household chore with scheduling and assignment details."""



    id: int
    chore_id: int
    tracked_time: datetime
    done_by: int 
    row_created_timestamp: datetime
    undone: bool
    undone_timestamp: datetime | None = None
    skipped: bool
    scheduled_execution_time: datetime | None = None
    userfields: dict | None = None

    chore: Chore | None = None
    done_by_user: User | None = None

    @classmethod
    def from_response(cls, resp) -> ChoreLog:
        """Create from a chores log API response."""
        return cls(
            id = resp.id,
            chore_id = resp.chore_id,
            tracked_time = resp.tracked_time,
            done_by = resp.done_by_user_id,
            row_created_timestamp = resp.row_created_timestamp,
            undone = resp.undone,
            undone_timestamp = resp.undone_timestamp,
            skipped = resp.skipped,
            scheduled_execution_time = resp.scheduled_execution_time,
            userfields = resp.userfields,

            chore = None,
            done_by_user = None,
        )

    def get_details(self, api_client: GrocyApiClient):
        self.userfields = api_client.get_userfields("chores_log", self.id)
        self.chore = Chore.from_details_response(api_client.get_chore(self.chore_id))
        user = api_client.get_user(self.done_by)
        self.done_by_user = User(id = user.id,
                                 username = user.username,
                                 first_name = user.first_name,
                                 last_name = user.last_name,
                                 display_name = user.display_name,
                                 ) 
