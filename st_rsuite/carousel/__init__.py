"""RSuite Carousel component for Streamlit."""

from __future__ import annotations

import base64
import mimetypes
import os
from typing import Callable

import streamlit as st

_component = st.components.v2.component(
    "st-rsuite.carousel",
    js="index-*.js",
    html='<div class="react-root"></div>',
    isolate_styles=False,
)


def _resolve_src(src: str) -> str:
    """Convert local file paths to base64 data URIs; leave URLs unchanged."""
    if src.startswith(("http://", "https://", "data:")):
        return src
    path = os.path.expanduser(src)
    if os.path.isfile(path):
        mime = mimetypes.guess_type(path)[0] or "image/jpeg"
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"data:{mime};base64,{b64}"
    return src


def carousel(
    items: list[dict],
    autoplay: bool = True,
    autoplay_interval: int = 4000,
    placement: str = "bottom",
    shape: str = "dot",
    active_index: int = 0,
    locale: str | None = None,
    on_change: Callable | None = None,
    key: str | None = None,
) -> int:
    """A content/image carousel powered by RSuite.

    Parameters
    ----------
    items : list of dict
        Carousel slides. Each dict can have:
        - 'content' (str): text content to display
        - 'src' (str): image URL or local file path
        - 'alt' (str): image alt text
        - 'background' (str): background color (default '#8b5cf6')
        - 'color' (str): text color (default '#fff')
    autoplay : bool
        Auto-transition between slides.
    autoplay_interval : int
        Milliseconds between auto-transitions.
    placement : str
        Indicator position: 'top', 'bottom', 'left', 'right'.
    shape : str
        Indicator shape: 'dot' or 'bar'.
    active_index : int
        Initially active slide index.
    locale : str or None
        RSuite locale key.
    on_change : callable or None
        Callback when the active slide changes.
    key : str or None
        Unique widget key.

    Returns
    -------
    int
        The active slide index.
    """

    def _noop():
        pass

    resolved_items = []
    for item in items:
        if "src" in item:
            resolved_items.append({**item, "src": _resolve_src(item["src"])})
        else:
            resolved_items.append(item)

    result = _component(
        key=key,
        default={"active_index": active_index},
        data={
            "items": resolved_items,
            "autoplay": autoplay,
            "autoplayInterval": autoplay_interval,
            "placement": placement,
            "shape": shape,
            "activeIndex": active_index,
            "locale": locale,
        },
        on_active_index_change=on_change or _noop,
    )

    idx = result.get("active_index") if result else active_index
    return idx if idx is not None else active_index
