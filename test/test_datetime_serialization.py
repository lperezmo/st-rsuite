"""Unit guards for datetime mode on date_picker and date_range_picker.

Both pickers derive their mode from ``format``: when the format string carries a
time field, RSuite renders a time panel and the widget must serialize and return
a ``datetime`` rather than a ``date``. The detection rule is narrow on purpose:
``M`` is month and ``d`` is day, so only ``h H m s a`` (outside single-quoted
literals) count as time fields.

These tests cover the browser-less half: the format rule, the serializer, and
the return-trip parser. Everything here is pure Python, so no CCv2 registration
or Streamlit runtime is involved.
"""

from datetime import date, datetime, timedelta, timezone

import pytest

from st_rsuite._dates import (
    format_has_time,
    parse_date_return,
    parse_datetime_return,
    serialize_date,
    serialize_datetime,
)

DATE_ONLY_FORMATS = [
    "yyyy-MM-dd",
    "MM/dd/yyyy",
    "dd.MM.yyyy",
    "yyyy",
    "MMMM yyyy",
    "yyyy-MM",
]

TIME_FORMATS = [
    "yyyy-MM-dd HH:mm",
    "yyyy-MM-dd HH:mm:ss",
    "yyyy-MM-dd hh:mm aa",
    "dd.MM.yyyy H:m",
    "yyyy-MM-dd'T'HH:mm",
]


@pytest.mark.parametrize("fmt", DATE_ONLY_FORMATS)
def test_date_only_formats_are_not_datetime_mode(fmt: str):
    assert format_has_time(fmt) is False


@pytest.mark.parametrize("fmt", TIME_FORMATS)
def test_time_formats_are_datetime_mode(fmt: str):
    assert format_has_time(fmt) is True


def test_month_and_day_tokens_alone_never_trigger_datetime_mode():
    """The trap: 'M' is month and 'd' is day, not minute and day-of-time."""
    assert format_has_time("MM-dd") is False
    assert format_has_time("dd MMM yyyy") is False


def test_rule_matches_rsuite_quoted_literals_included():
    """RSuite's shouldRenderTime tests the raw string, so a quoted literal
    containing h/H/m/s makes it show a time panel. Python must agree, or the
    picked time would be dropped on the round trip."""
    assert format_has_time("yyyy-MM-dd 'March'") is True
    assert format_has_time("'hms' yyyy-MM-dd") is True
    assert format_has_time("yyyy-MM-dd 'at' HH:mm") is True
    # 'a' alone is an AM/PM marker without an hour field: no time panel.
    assert format_has_time("yyyy-MM-dd a") is False


def test_empty_or_missing_format_is_date_only():
    assert format_has_time("") is False
    assert format_has_time(None) is False


def test_datetime_default_round_trips():
    value = datetime(2026, 6, 1, 8, 30)
    serialized = serialize_datetime(value)
    assert serialized == "2026-06-01T08:30:00"
    assert parse_datetime_return(serialized) == value


def test_datetime_serialization_always_carries_seconds():
    assert serialize_datetime(datetime(2026, 6, 1, 8, 30)).endswith(":00")
    assert serialize_datetime(datetime(2026, 6, 1, 8, 30, 45)) == "2026-06-01T08:30:45"


def test_microseconds_are_truncated_not_rendered():
    assert serialize_datetime(datetime(2026, 6, 1, 8, 30, 45, 123456)) == (
        "2026-06-01T08:30:45"
    )


def test_tz_aware_datetime_keeps_wall_time_and_drops_the_offset():
    aware = datetime(2026, 6, 1, 8, 30, tzinfo=timezone(timedelta(hours=-8)))
    assert serialize_datetime(aware) == "2026-06-01T08:30:00"
    assert serialize_datetime(datetime(2026, 6, 1, 8, 30, tzinfo=timezone.utc)) == (
        "2026-06-01T08:30:00"
    )


def test_plain_date_in_datetime_mode_gets_midnight():
    assert serialize_datetime(date(2026, 6, 1)) == "2026-06-01T00:00:00"
    assert parse_datetime_return("2026-06-01T00:00:00") == datetime(2026, 6, 1, 0, 0)


def test_date_string_in_datetime_mode_gets_midnight():
    assert serialize_datetime("2026-06-01") == "2026-06-01T00:00:00"


def test_datetime_string_is_normalized():
    assert serialize_datetime("2026-06-01T08:30") == "2026-06-01T08:30:00"
    assert serialize_datetime("2026-06-01 08:30:45") == "2026-06-01T08:30:45"


def test_none_stays_none_in_datetime_mode():
    assert serialize_datetime(None) is None


def test_unparseable_string_passes_through_like_serialize_date():
    """serialize_date hands an unknown string to the frontend as-is; the
    datetime serializer must not start raising where the date one did not."""
    assert serialize_datetime("not a date") == "not a date"
    assert serialize_date("not a date") == "not a date"


def test_date_mode_parser_returns_a_date():
    parsed = parse_date_return("2026-06-01")
    assert parsed == date(2026, 6, 1)
    assert not isinstance(parsed, datetime)


def test_datetime_mode_parser_returns_a_datetime():
    parsed = parse_datetime_return("2026-06-01T08:30:00")
    assert isinstance(parsed, datetime)
    assert parsed == datetime(2026, 6, 1, 8, 30)


def test_datetime_mode_parser_accepts_a_bare_day():
    """A datetime picker whose value was never touched can still see a plain
    day come back; it lands at midnight rather than vanishing."""
    assert parse_datetime_return("2026-06-01") == datetime(2026, 6, 1, 0, 0)


@pytest.mark.parametrize("bad", ["", None, "not a date", "2026-13-40", "08:30"])
def test_invalid_values_return_none_on_both_parsers(bad):
    assert parse_date_return(bad) is None
    assert parse_datetime_return(bad) is None


def test_date_parser_rejects_a_timestamp():
    """Date mode never sees a timestamp; if it does, None is the honest answer
    rather than a silently truncated day."""
    assert parse_date_return("2026-06-01T08:30:00") is None
