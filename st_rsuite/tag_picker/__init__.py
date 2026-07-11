"""RSuite TagPicker component for Streamlit."""

from __future__ import annotations

from typing import Callable

from st_rsuite._component import bind_kind

_component = bind_kind("tag_picker")


def tag_picker(
    items: list[dict],
    value: list[str] | None = None,
    label: str = "",
    searchable: bool = True,
    virtualized: bool = False,
    creatable: bool = False,
    disabled_items: list[str] | None = None,
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
    """A searchable multi-select rendered as removable tags, powered by RSuite.

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
    creatable : bool
        Let the user create new options by typing a value not in ``items``.
        Created values come back in the return list like any other selection.
    disabled_items : list of str or None
        Option values rendered as non-selectable.
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
        Selected values (including any user-created ones when ``creatable``).
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
            "creatable": creatable,
            "disabledItems": disabled_items or [],
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
        on_selected_values_change=on_change or _noop,
    )

    selected = result.get("selected_values") if result else []
    return selected if selected else []
