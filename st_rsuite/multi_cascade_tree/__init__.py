"""RSuite MultiCascadeTree component for Streamlit."""

from __future__ import annotations

from typing import Callable

import streamlit as st

_component = st.components.v2.component(
    "st-rsuite.multi_cascade_tree",
    js="index-*.js",
    html='<div class="react-root"></div>',
    isolate_styles=False,
)


def multi_cascade_tree(
    data: list[dict],
    value: list[str] | None = None,
    cascade: bool = True,
    searchable: bool = False,
    column_width: int = 156,
    column_height: int = 320,
    disabled: bool = False,
    uncheckable_values: list[str] | None = None,
    locale: str | None = None,
    on_change: Callable | None = None,
    key: str | None = None,
) -> list[str]:
    """A multi-select cascading tree powered by RSuite.

    Parameters
    ----------
    data : list of dict
        Cascade options. Each dict must have 'value' and 'label' keys.
        Optional 'children' key for nested levels.
    value : list of str or None
        Default selected values.
    cascade : bool
        Whether parent/child selections cascade.
    searchable : bool
        Show search input.
    column_width : int
        Width of each cascade column in pixels.
    column_height : int
        Height of each cascade column in pixels.
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
        Selected values.
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
            "columnWidth": column_width,
            "columnHeight": column_height,
            "disabled": disabled,
            "uncheckableValues": uncheckable_values or [],
            "locale": locale,
        },
        on_selected_values_change=on_change or _noop,
    )

    selected = result.get("selected_values") if result else []
    return selected if selected else []
