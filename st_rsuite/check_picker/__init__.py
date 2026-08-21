"""RSuite CheckPicker component for Streamlit."""

from __future__ import annotations

from collections.abc import Callable

from st_rsuite._component import bind_kind

_component = bind_kind("check_picker")


def check_picker(
    items: list[dict],
    value: list[str] | None = None,
    label: str = "",
    searchable: bool = True,
    virtualized: bool = False,
    countable: bool = True,
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
) -> list[str]:
    """A searchable multi-select dropdown with checkboxes, powered by RSuite.

    Unlike ``tag_picker``, the selection is shown as a count (or placeholder)
    in the closed control instead of one tag per selected value, which keeps
    compact layouts tidy when many options are checked.

    Parameters
    ----------
    items : list of dict
        Options. Each dict must have 'value' and 'label' keys. An optional
        'group' key groups options under a shared heading; grouping turns on
        automatically when any item carries one.
    value : list of str or None
        Default selected values.
    label : str
        Label displayed above the control.
    searchable : bool
        Show a search input in the dropdown.
    virtualized : bool
        Render the option list virtualized; keeps large lists (thousands of
        items) fast.
    countable : bool
        Show the number of checked options in the closed control.
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
        Callback when the selection changes.
    key : str or None
        Unique widget key.

    Returns
    -------
    list of str
        Selected values, in the order they were checked.
    """

    def _noop():
        pass

    result = _component(
        key=key,
        default={"selected_values": value or []},
        data={
            "label": label,
            "items": items,
            "value": value or [],
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
            "countable": countable,
            "help": help,
            "locale": locale,
        },
        on_selected_values_change=on_change or _noop,
    )

    selected = result.get("selected_values") if result else []
    return selected if selected else []
