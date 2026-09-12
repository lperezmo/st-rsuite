"""RSuite DateRangePicker component for Streamlit."""

from __future__ import annotations

from collections.abc import Callable
from datetime import date, datetime

from st_rsuite._callbacks import single_fire
from st_rsuite._component import bind_kind
from st_rsuite._dates import (
    format_has_time,
    parse_date_return,
    parse_datetime_return,
    serialize_datetime,
)
from st_rsuite._dates import serialize_date as _serialize

_component = bind_kind("date_range_picker")


def date_range_picker(
    label: str = "",
    value: tuple[date | datetime | str | None, date | datetime | str | None]
    | None = None,
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
    editable: bool = True,
    loading: bool = False,
    help: str | None = None,
    min_date: date | str | None = None,
    max_date: date | str | None = None,
    disabled_dates: list[date | str] | None = None,
    disabled_weekdays: list[int] | None = None,
    limit_start_year: int | None = None,
    limit_end_year: int | None = None,
    ranges: list[dict] | None = None,
    default_calendar_value: tuple[date | datetime | str, date | datetime | str]
    | None = None,
    locale: str | None = None,
    on_change: Callable | None = None,
    key: str | None = None,
    show_meridiem: bool = False,
) -> tuple[date | None, date | None] | tuple[datetime | None, datetime | None]:
    """A date range picker with dual-calendar popup powered by RSuite.

    Datetime mode
    -------------
    When ``format`` contains a time field, RSuite renders time panels and the
    widget becomes a date-time range picker: it returns two ``datetime`` values
    instead of two ``date`` values, and ``value`` round-trips the times. The
    rule is RSuite's own: a format counts as a time format when it contains any
    of ``H h m s`` anywhere, quoted literals included (``M`` is month and ``d``
    is day, so those do not count).

    >>> start, end = date_range_picker(
    ...     label="Shift window",
    ...     value=(datetime(2026, 6, 1, 8, 0), datetime(2026, 6, 1, 17, 0)),
    ...     format="yyyy-MM-dd HH:mm",
    ...     key="drp_datetime",
    ... )  # doctest: +SKIP
    >>> start  # doctest: +SKIP
    datetime.datetime(2026, 6, 1, 8, 0)

    Parameters
    ----------
    label : str
        Label displayed at the start of the toggle.
    value : tuple of (date/datetime/str/None, date/datetime/str/None) or None
        Default range. Each end accepts a ``date``, a ``datetime``, or an ISO
        string (``YYYY-MM-DD`` or ``YYYY-MM-DDTHH:MM:SS``). In datetime mode a
        plain date defaults the time to 00:00:00.
    format : str
        Date format string (Unicode Technical Standard #35 tokens). Including a
        time field (any of ``H h m s``) switches the widget to datetime mode.
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
    editable : bool
        Allow typing the dates into the input. When False the field is
        toggle-only. Default True.
    loading : bool
        Show a loading-state indicator on the control. Default False.
    help : str or None
        Tooltip shown on an info marker next to the label (like Streamlit's
        ``help=``). Requires a label to attach to.
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
    ranges : list of dict or None
        Shortcut presets shown beside the calendar. Each dict is
        ``{"label": str, "value": (start, end)}`` where start/end are date
        objects or ISO strings; optional keys ``close_overlay`` (bool) and
        ``placement`` ('bottom' | 'left'). ``None`` keeps RSuite's built-in
        shortcuts (Today, Yesterday, Last 7 days); an empty list ``[]`` removes
        them and shows no shortcut sidebar.
    default_calendar_value : tuple of (date/datetime/str, date/datetime/str) or None
        Which month pair the calendar panels open on when there is no
        selection. Does not select a value.
    locale : str or None
        RSuite locale key (e.g. 'ja_JP', 'zh_CN', 'es_ES'). None for English.
    on_change : callable or None
        Callback when the selected date range changes.
    key : str or None
        Unique widget key.
    show_meridiem : bool
        Show a 12-hour clock with an AM/PM column in the time panel. Pair it
        with a 12-hour ``format`` such as ``"yyyy-MM-dd hh:mm aa"``. Default
        False (24-hour clock).

    Returns
    -------
    tuple of (date or None, date or None)
        The selected start and end. Both are ``datetime`` in datetime mode.
    """
    with_time = format_has_time(format)
    # min/max/disabled dates stay day-granular: the frontend compares them on
    # the calendar day only, so a time component there would be meaningless.
    _serialize_value = serialize_datetime if with_time else _serialize

    start_val = None
    end_val = None
    if value is not None:
        start_val = _serialize_value(value[0])
        end_val = _serialize_value(value[1])

    # ranges: None keeps RSuite's defaults; a list (incl. empty) replaces them.
    serialized_ranges = None
    if ranges is not None:
        serialized_ranges = []
        for r in ranges:
            r_start, r_end = r["value"]
            preset = {
                "label": r["label"],
                "value": [_serialize_value(r_start), _serialize_value(r_end)],
            }
            if "close_overlay" in r:
                preset["closeOverlay"] = r["close_overlay"]
            if "placement" in r:
                preset["placement"] = r["placement"]
            serialized_ranges.append(preset)

    default_cal = None
    if default_calendar_value is not None:
        default_cal = [
            _serialize_value(default_calendar_value[0]),
            _serialize_value(default_calendar_value[1]),
        ]

    # Both ends share one callback: CCv2 dispatches per state key, so the end
    # date changing on its own must still reach on_change. single_fire keeps a
    # both-ends change from firing it twice.
    _fire_change = single_fire(on_change)

    result = _component(
        key=key,
        default={"start_date": start_val, "end_date": end_val},
        data={
            "label": label,
            "startValue": start_val,
            "endValue": end_val,
            "format": format,
            "withTime": with_time,
            "showMeridiem": show_meridiem,
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
            "editable": editable,
            "loading": loading,
            "help": help,
            "minDate": _serialize(min_date),
            "maxDate": _serialize(max_date),
            "disabledDates": [_serialize(d) for d in (disabled_dates or [])],
            "disabledWeekdays": disabled_weekdays or [],
            "limitStartYear": limit_start_year,
            "limitEndYear": limit_end_year,
            "ranges": serialized_ranges,
            "defaultCalendarValue": default_cal,
            "locale": locale,
        },
        on_start_date_change=_fire_change,
        on_end_date_change=_fire_change,
    )

    _parse = parse_datetime_return if with_time else parse_date_return

    if result:
        return (_parse(result.get("start_date")), _parse(result.get("end_date")))
    return (None, None)
