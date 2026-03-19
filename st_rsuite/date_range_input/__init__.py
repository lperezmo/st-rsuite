"""RSuite DateRangeInput component for Streamlit."""

from __future__ import annotations

from datetime import date
from typing import Callable

import streamlit as st

_component = st.components.v2.component(
    "st-rsuite.date_range_input",
    js="index-*.js",

    html='<div class="react-root"></div>',
    isolate_styles=False,
)


def date_range_input(
    label: str = "",
    value: tuple[date | str | None, date | str | None] | None = None,
    format: str = "yyyy-MM-dd",
    character: str = " ~ ",
    size: str = "md",
    placeholder: str | None = None,
    disabled: bool = False,
    locale: str | None = None,
    on_change: Callable | None = None,
    key: str | None = None,
) -> tuple[date | None, date | None]:
    """A keyboard-driven date range input powered by RSuite.

    Users navigate and edit date segments for both start and end dates using
    arrow keys and typing. No calendar popup.

    Parameters
    ----------
    label : str
        Label displayed above the input.
    value : tuple of (date/str/None, date/str/None) or None
        Default date range.
    format : str
        Date format string (Unicode Technical Standard #35 tokens).
    character : str
        Separator between start and end dates.
    size : str
        Input size: 'lg', 'md', 'sm', or 'xs'.
    placeholder : str or None
        Placeholder text when empty.
    disabled : bool
        Whether the input is disabled.
    locale : str or None
        RSuite locale key (e.g. 'ja_JP', 'zh_CN', 'es_ES'). None for English.
    on_change : callable or None
        Callback when the selected date range changes.
    key : str or None
        Unique widget key.

    Returns
    -------
    tuple of (date or None, date or None)
        The selected start and end dates.
    """
    def _serialize(d):
        if d is None:
            return None
        if isinstance(d, date):
            return d.isoformat()
        return str(d)

    start_val = None
    end_val = None
    if value is not None:
        start_val = _serialize(value[0])
        end_val = _serialize(value[1])

    def _noop():
        pass

    result = _component(
        key=key,
        default={"start_date": start_val, "end_date": end_val},
        data={
            "label": label,
            "startValue": start_val,
            "endValue": end_val,
            "format": format,
            "character": character,
            "size": size,
            "placeholder": placeholder or "",
            "disabled": disabled,
            "locale": locale,
        },
        on_start_date_change=on_change or _noop,
        on_end_date_change=_noop,
    )

    def _parse(val):
        if not val:
            return None
        try:
            return date.fromisoformat(val)
        except (ValueError, TypeError):
            return None

    if result:
        return (_parse(result.get("start_date")), _parse(result.get("end_date")))
    return (None, None)
