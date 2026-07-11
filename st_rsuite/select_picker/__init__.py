"""RSuite SelectPicker component for Streamlit."""

from __future__ import annotations

from typing import Callable

from st_rsuite._component import bind_kind

_component = bind_kind("select_picker")


def select_picker(
    items: list[dict],
    value: str | None = None,
    label: str = "",
    searchable: bool = True,
    virtualized: bool = False,
    disabled_items: list[str] | None = None,
    appearance: str = "default",
    size: str = "md",
    placeholder: str = "Select",
    placement: str = "bottomStart",
    disabled: bool = False,
    cleanable: bool = True,
    block: bool = False,
    loading: bool = False,
    help: str | None = None,
    locale: str | None = None,
    on_change: Callable | None = None,
    key: str | None = None,
) -> str | None:
    """A searchable single-select dropdown powered by RSuite.

    Parameters
    ----------
    items : list of dict
        Options. Each dict must have 'value' and 'label' keys. An optional
        'group' key groups options under a shared heading; grouping turns on
        automatically when any item carries one.
    value : str or None
        Default selected value.
    label : str
        Label displayed above the control.
    searchable : bool
        Show a search input in the dropdown.
    virtualized : bool
        Render the option list virtualized; keeps large lists (thousands of
        items) fast.
    disabled_items : list of str or None
        Option values rendered as non-selectable.
    appearance : str
        Visual style: 'default' or 'subtle'.
    size : str
        Component size: 'lg', 'md', 'sm', or 'xs'.
    placeholder : str
        Placeholder text.
    placement : str
        Popup placement (e.g. 'bottomStart', 'topEnd').
    disabled : bool
        Disable the component.
    cleanable : bool
        Show clear button.
    block : bool
        Full width.
    loading : bool
        Show a loading-state indicator on the control.
    help : str or None
        Tooltip shown on an info marker next to the label (like Streamlit's
        ``help=``). Requires a label to attach to.
    locale : str or None
        RSuite locale key (e.g. 'ja_JP', 'zh_CN', 'es_ES'). None for English.
    on_change : callable or None
        Callback when the selected value changes.
    key : str or None
        Unique widget key.

    Returns
    -------
    str or None
        The selected value, or None if nothing selected.
    """

    def _noop():
        pass

    result = _component(
        key=key,
        default={"selected_value": value},
        data={
            "label": label,
            "items": items,
            "value": value,
            "groupBy": "group" if any("group" in item for item in items) else None,
            "searchable": searchable,
            "virtualized": virtualized,
            "disabledItems": disabled_items or [],
            "appearance": appearance,
            "size": size,
            "placeholder": placeholder,
            "placement": placement,
            "disabled": disabled,
            "cleanable": cleanable,
            "block": block,
            "loading": loading,
            "help": help,
            "locale": locale,
        },
        on_selected_value_change=on_change or _noop,
    )

    return result.get("selected_value") if result else None
