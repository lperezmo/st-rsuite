"""Fast, browser-less guard that a real ``streamlit run`` would register every
st-rsuite component on the installed Streamlit.

This mirrors what the Streamlit runtime does at startup: it calls
``discover_and_register_components`` (see ``streamlit/runtime/runtime.py``) and
then resolves each component's ``asset_dir``. If discovery does not register a
component, a real app raises the reporter's
``Component 'st-rsuite.<name>' must be declared in pyproject.toml with asset_dir``
error. We assert all 13 resolve, and that the ``isolate_styles`` option the
components pass exists (Streamlit >= 1.53).

This is intentionally cheap (no server, no browser) so CI can run it across the
whole Streamlit version matrix. Note: ``streamlit.testing.v1.AppTest`` is NOT a
substitute here because it never runs discovery, so file-backed components always
look unregistered under it.
"""

import inspect

import streamlit as st
from streamlit.components.v2.get_bidi_component_manager import (
    get_bidi_component_manager,
)

import st_rsuite  # noqa: F401  (import must not raise)

COMPONENTS = [
    "date_picker",
    "date_range_picker",
    "time_picker",
    "time_range_picker",
    "date_input",
    "date_range_input",
    "radio_tile",
    "check_tree",
    "check_tree_picker",
    "multi_cascade_tree",
    "carousel",
    "timeline",
    "pin_input",
]


def test_isolate_styles_option_supported():
    params = inspect.signature(st.components.v2.component).parameters
    assert "isolate_styles" in params, (
        f"st.components.v2.component has no isolate_styles parameter; "
        f"Streamlit {st.__version__} is too old (st-rsuite needs >= 1.53)"
    )


def test_discovery_registers_all_components():
    mgr = get_bidi_component_manager()
    try:
        mgr.discover_and_register_components(start_file_watching=False)
    except TypeError:
        # Older signatures without the keyword argument.
        mgr.discover_and_register_components()

    missing = [
        name
        for name in COMPONENTS
        if mgr.get_component_asset_root(f"st-rsuite.{name}") is None
    ]
    assert not missing, (
        f"discovery did not register {missing} on Streamlit {st.__version__}; "
        "a real app would raise 'must be declared ... with asset_dir' for these"
    )
