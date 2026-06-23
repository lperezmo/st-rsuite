"""Streamlit version-compat layer for registering st-rsuite components.

Every st-rsuite component renders with style isolation turned off (no Shadow
DOM). RSuite injects its stylesheet into ``document.head`` and portals its popups
(calendars, cascader panels, and similar) to ``document.body``; both live outside
a shadow root, so a sandboxed component would render them unstyled. Streamlit
exposes that toggle in two different places depending on the version:

* Streamlit >= 1.53: ``isolate_styles`` is a parameter of the registration call
  ``st.components.v2.component(...)``.
* Streamlit 1.51 / 1.52: the registration call does not accept it; it is a
  parameter of the per-call renderer instead.

``component()`` hides that difference. It registers the component and returns a
renderer that always applies ``isolate_styles=False``, whichever Streamlit is
installed. This is what lets st-rsuite support Streamlit 1.51 and newer.
"""

from __future__ import annotations

import inspect
from typing import Any, Callable

import streamlit as st

# Whether the registration function accepts isolate_styles (Streamlit >= 1.53).
# Resolved once at import time.
_REGISTRATION_TAKES_ISOLATE_STYLES = (
    "isolate_styles" in inspect.signature(st.components.v2.component).parameters
)


def component(name: str, **registration_kwargs: Any) -> Callable[..., Any]:
    """Register a file-backed st-rsuite component with Shadow DOM isolation
    disabled, across every supported Streamlit version.

    Parameters
    ----------
    name:
        Qualified component name, e.g. ``"st-rsuite.date_picker"``.
    **registration_kwargs:
        Forwarded to ``st.components.v2.component`` (``js``, ``html``, and
        optionally ``css``).

    Returns
    -------
    Callable
        The component renderer. Call it exactly as you would the object returned
        by ``st.components.v2.component``; ``isolate_styles=False`` is applied for
        you regardless of where the installed Streamlit expects it.
    """
    # The shim is the single source of truth for isolation, so drop any
    # isolate_styles a caller may have passed.
    registration_kwargs.pop("isolate_styles", None)

    if _REGISTRATION_TAKES_ISOLATE_STYLES:
        return st.components.v2.component(
            name, isolate_styles=False, **registration_kwargs
        )

    # Streamlit 1.51 / 1.52: isolate_styles belongs on the call site.
    renderer = st.components.v2.component(name, **registration_kwargs)

    def render(**call_kwargs: Any) -> Any:
        call_kwargs.setdefault("isolate_styles", False)
        return renderer(**call_kwargs)

    return render
