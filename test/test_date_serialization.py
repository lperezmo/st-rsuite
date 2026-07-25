"""Unit guard for the shared date serializer used by every date widget.

``datetime`` is a subclass of ``date``, so an ``isinstance(value, date)`` branch
placed first swallows ``datetime`` and emits a full ``YYYY-MM-DDTHH:MM:SS``
timestamp. The frontend renders that as an Invalid Date and
``date.fromisoformat`` rejects it on the way back, so a ``datetime`` default
silently vanished on both sides. These tests pin the narrower check.

``serialize_date`` is shared by date_input, date_range_input, date_picker and
date_range_picker, so one guard covers all four.
"""

from datetime import date, datetime, timedelta, timezone

import pytest

from st_rsuite._dates import serialize_date

DATETIMES = [
    datetime(2026, 1, 2, 3, 4, 5),
    datetime(2026, 1, 2, 0, 0, 0),
    datetime(2026, 1, 2, 23, 59, 59, 999999),
    datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc),
    datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone(timedelta(hours=-8))),
]


def test_date_serializes_to_an_iso_day():
    assert serialize_date(date(2026, 1, 2)) == "2026-01-02"


def test_naive_datetime_drops_the_time():
    assert serialize_date(datetime(2026, 1, 2, 3, 4, 5)) == "2026-01-02"


def test_tz_aware_datetime_drops_the_time_and_offset():
    aware = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone(timedelta(hours=-8)))
    assert serialize_date(aware) == "2026-01-02"


@pytest.mark.parametrize("value", DATETIMES)
def test_datetime_never_emits_a_time_component(value: datetime):
    """The exact regression: any time component at all breaks both sides."""
    serialized = serialize_date(value)
    assert "T" not in serialized, f"{value!r} serialized with a time: {serialized}"
    assert ":" not in serialized, f"{value!r} serialized with a time: {serialized}"
    assert len(serialized) == len("YYYY-MM-DD")


@pytest.mark.parametrize("value", DATETIMES)
def test_serialized_datetime_parses_back_to_its_own_day(value: datetime):
    """The widgets parse the return trip with date.fromisoformat, which raises
    on a timestamp and makes the widget return None."""
    assert date.fromisoformat(serialize_date(value)) == value.date()


def test_none_stays_none():
    assert serialize_date(None) is None


def test_iso_string_passes_through():
    assert serialize_date("2026-01-02") == "2026-01-02"
