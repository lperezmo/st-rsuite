"""RSuite TimeRangePicker component for Streamlit."""

from __future__ import annotations

from datetime import time
from typing import Callable

import streamlit as st

_component = st.components.v2.component(
    "st-rsuite.time_range_picker",
    js="index-*.js",

    html='<div class="react-root"></div>',
    isolate_styles=False,
)


def time_range_picker(
    label: str = "",
    value: tuple[time | str | None, time | str | None] | None = None,
    format: str = "HH:mm",
    character: str = " ~ ",
    appearance: str = "default",
    size: str = "md",
    placeholder: str = "",
    placement: str = "bottomStart",
    disabled: bool = False,
    cleanable: bool = True,
    block: bool = False,
    show_meridiem: bool = False,
    on_change: Callable | None = None,
    key: str | None = None,
) -> tuple[time | None, time | None]:
    """A time range picker with popup powered by RSuite.

    Parameters
    ----------
    label : str
        Label displayed at the start of the toggle.
    value : tuple of (time/str/None, time/str/None) or None
        Default time range.
    format : str
        Time format string (e.g. 'HH:mm', 'hh:mm aa').
    character : str
        Separator between start and end times.
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
    show_meridiem : bool
        Show AM/PM for 12-hour format.
    on_change : callable or None
        Callback when the selected time range changes.
    key : str or None
        Unique widget key.

    Returns
    -------
    tuple of (time or None, time or None)
        The selected start and end times.
    """
    def _serialize(t):
        if t is None:
            return None
        if isinstance(t, time):
            return t.isoformat()
        return str(t)

    start_val = None
    end_val = None
    if value is not None:
        start_val = _serialize(value[0])
        end_val = _serialize(value[1])

    def _noop():
        pass

    result = _component(
        key=key,
        default={"start_time": start_val, "end_time": end_val},
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
            "showMeridiem": show_meridiem,
        },
        on_start_time_change=on_change or _noop,
        on_end_time_change=_noop,
    )

    def _parse(val):
        if not val:
            return None
        try:
            return time.fromisoformat(val)
        except (ValueError, TypeError):
            return None

    if result:
        return (_parse(result.get("start_time")), _parse(result.get("end_time")))
    return (None, None)
