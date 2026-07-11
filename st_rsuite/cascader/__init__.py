"""RSuite Cascader component for Streamlit."""

from __future__ import annotations

from typing import Callable

from st_rsuite._component import bind_kind

_component = bind_kind("cascader")


def cascader(
    data: list[dict],
    value: str | None = None,
    label: str = "",
    parent_selectable: bool = False,
    searchable: bool = True,
    disabled_items: list[str] | None = None,
    column_width: int = 156,
    column_height: int = 320,
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
    """A single-select cascading column picker powered by RSuite.

    The single-select counterpart of ``multi_cascade_tree``: navigate through
    hierarchical levels column by column and pick one item.

    Parameters
    ----------
    data : list of dict
        Cascade options. Each dict must have 'value' and 'label' keys.
        Optional 'children' key for nested levels.
    value : str or None
        Default selected value.
    label : str
        Label displayed above the control.
    parent_selectable : bool
        Allow selecting non-leaf nodes. By default only leaves are
        selectable.
    searchable : bool
        Show a search input in the popup.
    disabled_items : list of str or None
        Node values rendered as non-selectable.
    column_width : int
        Width of each cascade column in pixels.
    column_height : int
        Height of each cascade column in pixels.
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
        The selected node value, or None if nothing selected.
    """

    def _noop():
        pass

    result = _component(
        key=key,
        default={"selected_value": value},
        data={
            "label": label,
            "data": data,
            "value": value,
            "parentSelectable": parent_selectable,
            "searchable": searchable,
            "disabledItems": disabled_items or [],
            "columnWidth": column_width,
            "columnHeight": column_height,
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
