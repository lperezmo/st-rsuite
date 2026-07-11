"""RSuite TreePicker component for Streamlit."""

from __future__ import annotations

from typing import Callable

from st_rsuite._component import bind_kind

_component = bind_kind("tree_picker")


def tree_picker(
    data: list[dict],
    value: str | None = None,
    label: str = "",
    searchable: bool = True,
    virtualized: bool = False,
    default_expand_all: bool = False,
    show_indent_line: bool = False,
    only_leaf_selectable: bool = False,
    disabled_items: list[str] | None = None,
    height: int = 320,
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
    """A dropdown picker with a single-select tree inside, powered by RSuite.

    The single-select counterpart of ``check_tree_picker``.

    Parameters
    ----------
    data : list of dict
        Tree nodes. Each dict must have 'value' and 'label' keys.
        Optional 'children' key for nested nodes.
    value : str or None
        Default selected value.
    label : str
        Label displayed above the control.
    searchable : bool
        Show a search input in the dropdown.
    virtualized : bool
        Render the tree virtualized; keeps very large trees fast.
    default_expand_all : bool
        Expand all tree nodes initially.
    show_indent_line : bool
        Show indent guide lines.
    only_leaf_selectable : bool
        Allow selecting leaf nodes only.
    disabled_items : list of str or None
        Node values rendered as non-selectable.
    height : int
        Tree height in pixels inside the dropdown.
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
            "searchable": searchable,
            "virtualized": virtualized,
            "defaultExpandAll": default_expand_all,
            "showIndentLine": show_indent_line,
            "onlyLeafSelectable": only_leaf_selectable,
            "disabledItems": disabled_items or [],
            "height": height,
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
