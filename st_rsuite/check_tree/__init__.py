"""RSuite CheckTree component for Streamlit."""

from __future__ import annotations

from typing import Callable

import streamlit as st

_component = st.components.v2.component(
    "st-rsuite.check_tree",
    js="index-*.js",
    html='<div class="react-root"></div>',
    isolate_styles=False,
)


def check_tree(
    data: list[dict],
    value: list[str] | None = None,
    cascade: bool = True,
    searchable: bool = True,
    default_expand_all: bool = False,
    show_indent_line: bool = False,
    height: int = 360,
    disabled: bool = False,
    uncheckable_values: list[str] | None = None,
    locale: str | None = None,
    on_change: Callable | None = None,
    key: str | None = None,
) -> list[str]:
    """A tree with checkboxes powered by RSuite.

    Parameters
    ----------
    data : list of dict
        Tree nodes. Each dict must have 'value' and 'label' keys.
        Optional 'children' key for nested nodes.
    value : list of str or None
        Default selected values.
    cascade : bool
        Whether parent/child selections cascade.
    searchable : bool
        Show search input.
    default_expand_all : bool
        Expand all tree nodes initially.
    show_indent_line : bool
        Show indent guide lines.
    height : int
        Tree height in pixels.
    disabled : bool
        Disable the component.
    uncheckable_values : list of str or None
        Values that cannot be checked.
    locale : str or None
        RSuite locale key (e.g. 'ja_JP').
    on_change : callable or None
        Callback when selection changes.
    key : str or None
        Unique widget key.

    Returns
    -------
    list of str
        Selected node values.
    """

    def _noop():
        pass

    result = _component(
        key=key,
        default={"selected_values": value or []},
        data={
            "data": data,
            "value": value or [],
            "cascade": cascade,
            "searchable": searchable,
            "defaultExpandAll": default_expand_all,
            "showIndentLine": show_indent_line,
            "height": height,
            "disabled": disabled,
            "uncheckableValues": uncheckable_values or [],
            "locale": locale,
        },
        on_selected_values_change=on_change or _noop,
    )

    selected = result.get("selected_values") if result else []
    return selected if selected else []
