"""RSuite DateInput component for Streamlit."""

from __future__ import annotations

from datetime import date
from typing import Callable

from st_rsuite._component import bind_kind

_component = bind_kind("date_input")


def date_input(
    label: str = "",
    value: date | str | None = None,
    format: str = "yyyy-MM-dd",
    size: str = "md",
    placeholder: str | None = None,
    disabled: bool = False,
    help: str | None = None,
    locale: str | None = None,
    on_change: Callable | None = None,
    key: str | None = None,
) -> date | None:
    """A keyboard-driven date input powered by RSuite.

    Users navigate and edit date segments (year, month, day) using arrow keys
    and typing. No calendar popup.

    Parameters
    ----------
    label : str
        Label displayed above the input.
    value : date or str or None
        Default date value. Accepts date object or ISO string (YYYY-MM-DD).
    format : str
        Date format string (Unicode Technical Standard #35 tokens).
    size : str
        Input size: 'lg', 'md', 'sm', or 'xs'.
    placeholder : str or None
        Placeholder text when empty.
    disabled : bool
        Whether the input is disabled.
    help : str or None
        Tooltip shown on an info marker next to the label (like Streamlit's
        ``help=``). Requires a label to attach to.
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
            "size": size,
            "placeholder": placeholder or "",
            "disabled": disabled,
            "help": help,
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
