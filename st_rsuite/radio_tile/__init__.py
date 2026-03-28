"""RSuite RadioTile component for Streamlit."""

from __future__ import annotations

from typing import Callable

import streamlit as st

_component = st.components.v2.component(
    "st-rsuite.radio_tile",
    js="index-*.js",
    html='<div class="react-root"></div>',
    isolate_styles=False,
)


def radio_tile(
    options: list[dict],
    value: str | None = None,
    inline: bool = False,
    disabled: bool = False,
    locale: str | None = None,
    on_change: Callable | None = None,
    key: str | None = None,
) -> str | None:
    """A tile-based radio group powered by RSuite.

    Parameters
    ----------
    options : list of dict
        Each dict must have 'value' and 'label' keys. Optional keys:
        'description' (str) and 'icon' (str, rendered as text/emoji).
    value : str or None
        Default selected tile value.
    inline : bool
        Arrange tiles horizontally instead of stacked.
    disabled : bool
        Whether the entire group is disabled.
    locale : str or None
        RSuite locale key (e.g. 'ja_JP'). None for default.
    on_change : callable or None
        Callback when the selected tile changes.
    key : str or None
        Unique widget key.

    Returns
    -------
    str or None
        The selected tile value, or None if nothing selected.
    """

    def _noop():
        pass

    result = _component(
        key=key,
        default={"selected_value": value},
        data={
            "options": options,
            "value": value,
            "inline": inline,
            "disabled": disabled,
            "locale": locale,
        },
        on_selected_value_change=on_change or _noop,
    )

    selected = result.get("selected_value") if result else None
    return selected if selected else None
