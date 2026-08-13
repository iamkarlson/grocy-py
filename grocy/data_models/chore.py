from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel

from .user import User


class PeriodType(str, Enum):
    """Chore recurrence period type."""

    MANUALLY = "manually"
    DYNAMIC_REGULAR = "dynamic-regular"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    ADAPTIVE = "adaptive"
    HOURLY = "hourly"


class AssignmentType(str, Enum):
    """Chore assignment strategy."""

    NO_ASSIGNMENT = "no-assignment"
    WHO_LEAST_DID_FIRST = "who-least-did-first"
    RANDOM = "random"
    IN_ALPHABETICAL_ORDER = "in-alphabetical-order"


class Chore(BaseModel):
    """A household chore with scheduling and assignment details."""

    id: int
    name: str | None = None
    description: str | None = None
    period_type: PeriodType | None = None
    period_config: str | None = None
    period_days: int | None = None
    period_interval: int | None = 0
    start_date: datetime | None = None
    consume_product_on_execution: bool | None = False
    product_id: int | None = None
    track_date_only: bool | None = None
    rollover: bool | None = None
    assignment_type: AssignmentType | None = None
    assignment_config: str | None = None
    next_execution_assigned_to_user_id: int | None = None
    userfields: dict | None = None
    last_tracked_time: datetime | None = None
    next_estimated_execution_time: datetime | None = None
    last_done_by: User | None = None
    track_count: int | None = None
    next_execution_assigned_user: User | None = None

    @classmethod
    def from_current_response(cls, resp) -> Chore:
        """Create from a current-chores API response."""
        return cls(
            id=resp.chore_id,
            last_tracked_time=resp.last_tracked_time,
            next_estimated_execution_time=resp.next_estimated_execution_time,
        )

    @classmethod
    def from_details_response(cls, resp) -> Chore:
        """Create from a chore-details API response."""
        chore_data = resp.chore
        period_type = (
            PeriodType(chore_data.period_type)
            if chore_data.period_type is not None
            else None
        )
        assignment_type = (
            AssignmentType(chore_data.assignment_type)
            if chore_data.assignment_type is not None
            else None
        )
        last_done_by = (
            User(
                id=resp.last_done_by.id,
                username=resp.last_done_by.username,
                first_name=resp.last_done_by.first_name,
                last_name=resp.last_done_by.last_name,
                display_name=resp.last_done_by.display_name,
            )
            if resp.last_done_by
            else None
        )
        next_user = (
            User(
                id=resp.next_execution_assigned_user.id,
                username=resp.next_execution_assigned_user.username,
                first_name=resp.next_execution_assigned_user.first_name,
                last_name=resp.next_execution_assigned_user.last_name,
                display_name=resp.next_execution_assigned_user.display_name,
            )
            if resp.next_execution_assigned_user
            else None
        )
        return cls(
            id=chore_data.id,
            name=chore_data.name,
            description=chore_data.description,
            period_type=period_type,
            period_config=chore_data.period_config,
            period_days=chore_data.period_days,
            period_interval=chore_data.period_interval,
            start_date=chore_data.start_date,
            consume_product_on_execution=chore_data.consume_product_on_execution,
            product_id=chore_data.product_id,
            track_date_only=chore_data.track_date_only,
            rollover=chore_data.rollover,
            assignment_type=assignment_type,
            assignment_config=chore_data.assignment_config,
            next_execution_assigned_to_user_id=chore_data.next_execution_assigned_to_user_id,
            userfields=chore_data.userfields,
            last_tracked_time=resp.last_tracked,
            next_estimated_execution_time=resp.next_estimated_execution_time,
            last_done_by=last_done_by,
            track_count=resp.track_count,
            next_execution_assigned_user=next_user,
        )

    def get_details(self, api_client):
        """Fetch and populate full chore details and userfields from the API."""
        details = api_client.get_chore(self.id)
        if details:
            updated = Chore.from_details_response(details)
            self.__dict__.update(updated.__dict__)
            self.userfields = api_client.get_userfields("chores", self.id)
