"""Fast, browser-less guard that a real ``streamlit run`` would register every
st-rsuite component on the installed Streamlit.

This mirrors what the Streamlit runtime does at startup: it calls
``discover_and_register_components`` (see ``streamlit/runtime/runtime.py``) and
then resolves each component's ``asset_dir``. If discovery does not register a
component, a real app raises the reporter's
``Component 'st-rsuite.<name>' must be declared in pyproject.toml with asset_dir``
error. We assert all 13 resolve, and that the installed Streamlit lets the compat
layer disable style isolation (at registration on Streamlit >= 1.53, or on the
per-call renderer on 1.51 / 1.52).

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
from st_rsuite import _compat

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


def test_isolate_styles_controllable():
    """st-rsuite renders every component with Shadow DOM isolation disabled. The
    toggle lives on the registration call (Streamlit >= 1.53) or on the per-call
    renderer (Streamlit 1.51 / 1.52); the compat layer must find it in one of
    those places on the installed Streamlit."""
    if _compat._REGISTRATION_TAKES_ISOLATE_STYLES:
        assert "isolate_styles" in inspect.signature(st.components.v2.component).parameters
    else:
        probe = st.components.v2.component(
            "probe.isolate", html="<div></div>", css="", js="console.log(0)"
        )
        assert "isolate_styles" in inspect.signature(probe).parameters, (
            f"Streamlit {st.__version__} exposes isolate_styles at neither "
            "registration nor the call site; st-rsuite cannot disable isolation"
        )


def test_compat_shim_registers_without_error():
    """The compat shim registers a component without raising on the installed
    Streamlit version (covers both the >=1.53 and 1.51/1.52 branches)."""
    renderer = _compat.component(
        "probe.compat", html="<div></div>", css="", js="console.log(0)"
    )
    assert callable(renderer)


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
