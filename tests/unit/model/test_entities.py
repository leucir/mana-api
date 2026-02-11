"""Unit tests for domain entities and aggregates (T055 subset)."""
from datetime import datetime
import pytest

from model.entities.intent import Intent
from model.entities.target import Target
from model.aggregates.inspection_session import InspectionSession, SessionStatus


def test_intent_requires_goal():
    with pytest.raises(ValueError, match="goal"):
        Intent(goal="", constraints=None)
    with pytest.raises(ValueError, match="goal"):
        Intent(goal="   ", constraints=None)
    intent = Intent(goal="Inspect vehicle", constraints={"time": "30m"})
    assert intent.goal == "Inspect vehicle"
    assert intent.constraints == {"time": "30m"}


def test_session_status_transitions():
    now = datetime.utcnow()
    session = InspectionSession(
        id="s1",
        tenant_id="t1",
        status=SessionStatus.CREATED,
        intent=Intent(goal="Check roof"),
        target=None,
        created_at=now,
        updated_at=now,
        created_by="u1",
        completed_at=None,
        record_id=None,
    )
    assert session.status == SessionStatus.CREATED
    session.start_progress()
    assert session.status == SessionStatus.IN_PROGRESS
    session.complete(record_id="r1")
    assert session.status == SessionStatus.COMPLETED
    assert session.record_id == "r1"
