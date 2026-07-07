"""RSuite TimePicker component for Streamlit."""

from __future__ import annotations

from datetime import time
from typing import Callable

from st_rsuite._compat import component

_component = component(
    "st-rsuite.time_picker",
    js="index-*.js",

    html='<div class="react-root"></div>',
)


def time_picker(
    label: str = "",
    value: time | str | None = None,
    format: str = "HH:mm",
    appearance: str = "default",
    size: str = "md",
    placeholder: str = "",
    placement: str = "bottomStart",
    disabled: bool = False,
    cleanable: bool = True,
    block: bool = False,
    show_meridiem: bool = False,
    editable: bool = True,
    loading: bool = False,
    min_hour: int | None = None,
    max_hour: int | None = None,
    hidden_hours: list[int] | None = None,
    hidden_minutes: list[int] | None = None,
    hidden_seconds: list[int] | None = None,
    locale: str | None = None,
    on_change: Callable | None = None,
    key: str | None = None,
) -> time | None:
    """A time picker with popup powered by RSuite.

    Parameters
    ----------
    label : str
        Label displayed at the start of the toggle.
    value : time or str or None
        Default time value. Accepts time object or HH:MM string.
    format : str
        Time format string (e.g. 'HH:mm', 'HH:mm:ss', 'hh:mm aa').
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
    editable : bool
        Allow typing the time into the input. When False the field is
        toggle-only (opens the panel; no keyboard entry). Default True.
    loading : bool
        Show a loading-state indicator on the control. Default False.
    min_hour : int or None
        Earliest selectable hour (0-23, inclusive). Earlier hours are hidden
        from the panel.
    max_hour : int or None
        Latest selectable hour (0-23, inclusive). Later hours are hidden.
    hidden_hours : list of int or None
        Specific hours (0-23) to hide from the panel.
    hidden_minutes : list of int or None
        Specific minutes (0-59) to hide from the panel.
    hidden_seconds : list of int or None
        Specific seconds (0-59) to hide from the panel.
    locale : str or None
        RSuite locale key (e.g. 'ja_JP', 'zh_CN', 'es_ES'). None for English.
    on_change : callable or None
        Callback when the selected time changes.
    key : str or None
        Unique widget key.

    Returns
    -------
    time or None
        The selected time, or None if nothing selected.
    """
    def _serialize(t):
        if t is None:
            return None
        if isinstance(t, time):
            return t.isoformat()
        return str(t)

    def _noop():
        pass

    result = _component(
        key=key,
        default={"selected_time": _serialize(value)},
        data={
            "label": label,
            "value": _serialize(value),
            "format": format,
            "appearance": appearance,
            "size": size,
            "placeholder": placeholder,
            "placement": placement,
            "disabled": disabled,
            "cleanable": cleanable,
            "block": block,
            "showMeridiem": show_meridiem,
            "editable": editable,
            "loading": loading,
            "minHour": min_hour,
            "maxHour": max_hour,
            "hiddenHours": hidden_hours or [],
            "hiddenMinutes": hidden_minutes or [],
            "hiddenSeconds": hidden_seconds or [],
            "locale": locale,
        },
        on_selected_time_change=on_change or _noop,
    )

    selected = result.get("selected_time") if result else None
    if selected:
        try:
            return time.fromisoformat(selected)
        except (ValueError, TypeError):
            return None
    return None
