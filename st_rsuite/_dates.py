"""Date serialization shared by the date-flavored widgets."""

from __future__ import annotations

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
