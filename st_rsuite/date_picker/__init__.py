"""RSuite DatePicker component for Streamlit."""

from __future__ import annotations

from datetime import date, datetime
from typing import Callable

from st_rsuite._compat import component

_component = component(
    "st-rsuite.date_picker",
    js="index-*.js",

    html='<div class="react-root"></div>',
)


def date_picker(
    label: str = "",
    value: date | str | None = None,
    format: str = "yyyy-MM-dd",
    appearance: str = "default",
    size: str = "md",
    placeholder: str = "",
    placement: str = "bottomStart",
    one_tap: bool = False,
    disabled: bool = False,
    cleanable: bool = True,
    block: bool = False,
    iso_week: bool = False,
    show_week_numbers: bool = False,
    editable: bool = True,
    loading: bool = False,
    min_date: date | str | None = None,
    max_date: date | str | None = None,
    disabled_dates: list[date | str] | None = None,
    disabled_weekdays: list[int] | None = None,
    limit_start_year: int | None = None,
    limit_end_year: int | None = None,
    locale: str | None = None,
    on_change: Callable | None = None,
    key: str | None = None,
) -> date | None:
    """A date picker with calendar popup powered by RSuite.

    Parameters
    ----------
    label : str
        Label displayed at the start of the toggle.
    value : date or str or None
        Default date value. Accepts date object or ISO string (YYYY-MM-DD).
    format : str
        Date format string (Unicode Technical Standard #35 tokens).
    appearance : str
        Visual style: 'default' or 'subtle'.
    size : str
        Component size: 'lg', 'md', 'sm', or 'xs'.
    placeholder : str
        Placeholder text.
    placement : str
        Popup placement (e.g. 'bottomStart', 'topEnd').
    one_tap : bool
        Single-click select (skip OK button).
    disabled : bool
        Whether the picker is disabled.
    cleanable : bool
        Show clear button.
    block : bool
        Full width.
    iso_week : bool
        Weeks start on Monday (ISO 8601).
    show_week_numbers : bool
        Show week numbers in the calendar.
    editable : bool
        Allow typing the date into the input. When False the field is
        toggle-only (opens the calendar; no keyboard entry). Default True.
    loading : bool
        Show a loading-state indicator on the control. Default False.
    min_date : date or str or None
        Earliest selectable date (inclusive). Earlier dates are disabled.
    max_date : date or str or None
        Latest selectable date (inclusive). Later dates are disabled.
    disabled_dates : list of date or str or None
        Individual dates to disable.
    disabled_weekdays : list of int or None
        Weekdays to disable, 0=Monday .. 6=Sunday (matching date.weekday()).
    limit_start_year : int or None
        Lower bound on the year navigable in the calendar, relative to the
        current selection.
    limit_end_year : int or None
        Upper bound on the year navigable in the calendar, relative to the
        current selection.
    locale : str or None
        RSuite locale key (e.g. 'ja_JP', 'zh_CN', 'es_ES'). None for English.
    on_change : callable or None
        Callback when the selected date changes.
    key : str or None
        Unique widget key.

    Returns
    -------
    date or None
        The selected date, or None if nothing selected.
    """
    def _serialize(d):
        if d is None:
            return None
        if isinstance(d, datetime):
            return d.date().isoformat()
        if isinstance(d, date):
            return d.isoformat()
        return str(d)

    def _noop():
        pass

    result = _component(
        key=key,
        default={"selected_date": _serialize(value)},
        data={
            "label": label,
            "value": _serialize(value),
            "format": format,
            "appearance": appearance,
            "size": size,
            "placeholder": placeholder,
            "placement": placement,
            "oneTap": one_tap,
            "disabled": disabled,
            "cleanable": cleanable,
            "block": block,
            "isoWeek": iso_week,
            "showWeekNumbers": show_week_numbers,
            "editable": editable,
            "loading": loading,
            "minDate": _serialize(min_date),
            "maxDate": _serialize(max_date),
            "disabledDates": [_serialize(d) for d in (disabled_dates or [])],
            "disabledWeekdays": disabled_weekdays or [],
            "limitStartYear": limit_start_year,
            "limitEndYear": limit_end_year,
            "locale": locale,
        },
        on_selected_date_change=on_change or _noop,
    )

    selected = result.get("selected_date") if result else None
    if selected:
        try:
            return date.fromisoformat(selected)
        except (ValueError, TypeError):
            return None
    return None
