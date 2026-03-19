"""RSuite DateRangePicker component for Streamlit."""

from __future__ import annotations

from datetime import date
from typing import Callable

import streamlit as st

_component = st.components.v2.component(
    "st-rsuite.date_range_picker",
    js="index-*.js",

    html='<div class="react-root"></div>',
    isolate_styles=False,
)


def date_range_picker(
    label: str = "",
    value: tuple[date | str | None, date | str | None] | None = None,
    format: str = "yyyy-MM-dd",
    character: str = " ~ ",
    appearance: str = "default",
    size: str = "md",
    placeholder: str = "",
    placement: str = "bottomStart",
    disabled: bool = False,
    cleanable: bool = True,
    block: bool = False,
    iso_week: bool = False,
    show_week_numbers: bool = False,
    show_one_calendar: bool = False,
    one_tap: bool = False,
    hover_range: str | None = None,
    on_change: Callable | None = None,
    key: str | None = None,
) -> tuple[date | None, date | None]:
    """A date range picker with dual-calendar popup powered by RSuite.

    Parameters
    ----------
    label : str
        Label displayed at the start of the toggle.
    value : tuple of (date/str/None, date/str/None) or None
        Default date range.
    format : str
        Date format string (Unicode Technical Standard #35 tokens).
    character : str
        Separator between start and end dates.
    appearance : str
        Visual style: 'default' or 'subtle'.
    size : str
        Component size: 'lg', 'md', 'sm', or 'xs'.
    placeholder : str
        Placeholder text.
    placement : str
        Popup placement.
    disabled : bool
        Whether the picker is disabled.
    cleanable : bool
        Show clear button.
    block : bool
        Full width.
    iso_week : bool
        Weeks start on Monday (ISO 8601).
    show_week_numbers : bool
        Show week numbers.
    show_one_calendar : bool
        Show only one calendar panel instead of two.
    one_tap : bool
        Single-click select.
    hover_range : str or None
        Hover highlight mode: 'week', 'month', or None.
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
            "appearance": appearance,
            "size": size,
            "placeholder": placeholder,
            "placement": placement,
            "disabled": disabled,
            "cleanable": cleanable,
            "block": block,
            "isoWeek": iso_week,
            "showWeekNumbers": show_week_numbers,
            "showOneCalendar": show_one_calendar,
            "oneTap": one_tap,
            "hoverRange": hover_range,
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
