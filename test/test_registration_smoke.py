"""Fast, browser-less guard that a real ``streamlit run`` would register the
shared st-rsuite component on the installed Streamlit.

This mirrors what the Streamlit runtime does at startup: it calls
``discover_and_register_components`` (see ``streamlit/runtime/runtime.py``) and
then resolves the component's ``asset_dir``. If discovery does not register it,
a real app raises the reporter's
``Component 'st-rsuite.rsuite' must be declared in pyproject.toml with asset_dir``
error for every widget (all 13 render through this single registration; the
frontend routes on the ``kind`` discriminator). We assert it resolves, that every
widget module binds a kind, and that the installed Streamlit lets the compat
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

WIDGETS = [
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


def test_discovery_registers_shared_component():
    mgr = get_bidi_component_manager()
    try:
        mgr.discover_and_register_components(start_file_watching=False)
    except TypeError:
        # Older signatures without the keyword argument.
        mgr.discover_and_register_components()

    assert mgr.get_component_asset_root("st-rsuite.rsuite") is not None, (
        f"discovery did not register st-rsuite.rsuite on Streamlit "
        f"{st.__version__}; a real app would raise 'must be declared ... with "
        "asset_dir' for every widget"
    )


def test_every_widget_binds_a_kind():
    """Each widget module's _component must inject its own kind so the shared
    frontend bundle dispatches to the right React component.

    File-backed registration raises outside a real ``streamlit run`` (pytest
    never runs asset discovery), so the shared registration is stubbed BEFORE
    st_rsuite._component first imports; the widget modules then bind their
    kinds against the stub.
    """
    import importlib
    import sys
    from unittest.mock import patch

    calls: list[dict] = []

    def fake_registration(name, **kwargs):
        assert name == "st-rsuite.rsuite"

        def render(**call_kwargs):
            calls.append(call_kwargs)

        return render

    # Force a clean import of the shared component and the widget modules so
    # they wire up against the stub, whatever ran earlier in the session.
    for mod in ["st_rsuite._component", *(f"st_rsuite.{w}" for w in WIDGETS)]:
        sys.modules.pop(mod, None)

    with patch.object(_compat, "component", fake_registration):
        for name in WIDGETS:
            module = importlib.import_module(f"st_rsuite.{name}")
            calls.clear()
            module._component(data={"probe": 1}, key="k")
            assert len(calls) == 1, f"{name} did not call the shared component"
            sent = calls[0]["data"]
            assert sent["kind"] == name, (
                f"{name} sent kind={sent.get('kind')!r}; the frontend would "
                "dispatch to the wrong widget"
            )
            assert sent["probe"] == 1, f"{name} dropped the caller's data"
