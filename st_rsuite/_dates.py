"""Date serialization shared by the date-flavored widgets."""

from __future__ import annotations

import re
from datetime import date, datetime


def serialize_date(value: date | str | None) -> str | None:
    """Serialize a date-ish default to the ISO ``YYYY-MM-DD`` string the
    frontend parses.

    ``datetime`` is checked before ``date`` because ``datetime`` is a subclass
    of ``date``: without the narrower check first, a ``datetime`` default would
    serialize to a full ``YYYY-MM-DDTHH:MM:SS`` timestamp, which the frontend
    cannot parse and which ``date.fromisoformat`` rejects on the way back. The
    default would then silently vanish on both sides.
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return str(value)


# RSuite decides whether to render a time panel with the same test
# (``shouldRenderTime`` in internals/utils/date/formatCheck.js): any of
# ``H h m s`` anywhere in the raw format string, quoted literals included.
# ``M`` is month and ``d`` is day, so those never count. Mirroring the rule
# exactly, quirks included, is what keeps the two sides in agreement: a format
# that makes RSuite show a time panel must make Python expect a datetime back.
_TIME_TOKEN = re.compile(r"[Hhms]")


def format_has_time(format_string: str | None) -> bool:
    """Whether a picker ``format`` makes RSuite render a time panel.

    Same rule as RSuite: any of ``H h m s`` in the format string. The widget
    then selects and returns a ``datetime`` instead of a ``date``.
    """
    if not format_string:
        return False
    return _TIME_TOKEN.search(format_string) is not None


def serialize_datetime(value: date | datetime | str | None) -> str | None:
    """Serialize a date-ish default to the ``YYYY-MM-DDTHH:MM:SS`` string the
    frontend parses in datetime mode.

    Local wall time, seconds always present, no timezone suffix. A plain
    ``date`` (or ``YYYY-MM-DD`` string) is valid and lands at midnight; a
    tz-aware ``datetime`` keeps its wall time and drops the offset, matching
    what ``serialize_date`` does with the offset today. Anything unparseable is
    passed through as a string, as ``serialize_date`` does.
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.replace(tzinfo=None).isoformat(timespec="seconds")
    if isinstance(value, date):
        return f"{value.isoformat()}T00:00:00"
    text = str(value).strip()
    try:
        parsed = datetime.fromisoformat(text.replace(" ", "T"))
    except ValueError:
        return text
    return parsed.replace(tzinfo=None).isoformat(timespec="seconds")


def parse_date_return(value: str | None) -> date | None:
    """Parse a frontend ``YYYY-MM-DD`` return value. ``None`` when unparseable."""
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except (ValueError, TypeError):
        return None


def parse_datetime_return(value: str | None) -> datetime | None:
    """Parse a frontend ``YYYY-MM-DDTHH:MM:SS`` return value.

    A bare ``YYYY-MM-DD`` is accepted and lands at midnight. ``None`` when
    unparseable, matching the date-only path.
    """
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except (ValueError, TypeError):
        return None
