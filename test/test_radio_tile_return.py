"""Unit guard for radio_tile's return value.

``return selected if selected else None`` made a legitimately selected
``{"value": "", "label": "None of the above"}`` tile indistinguishable from no
selection at all. Only a missing selection means "nothing selected"; the empty
string is a real option value and has to survive the round trip.

The widget module is imported against a stubbed CCv2 registration because
file-backed registration only resolves inside a real ``streamlit run`` (see
test_registration_smoke); ``registration_stub`` owns the import and the cleanup.
"""

import sys
from collections.abc import Callable
from types import ModuleType

import pytest
from registration_stub import stubbed_registration

import st_rsuite

_MISSING = object()

OPTIONS = [
    {"value": "a", "label": "Option A"},
    {"value": "", "label": "None of the above"},
]


def _radio_tile_returning(state: dict | None) -> Callable:
    """Import radio_tile bound to a stub component that returns ``state``."""

    def fake_registration(name, **kwargs):
        def render(**call_kwargs):
            return state

        return render

    with stubbed_registration("radio_tile", fake_registration) as module:
        return module.radio_tile


def test_empty_string_selection_is_returned_as_is():
    """The regression: a selected "None of the above" tile came back as None,
    so the app could not tell it from an untouched widget."""
    radio_tile = _radio_tile_returning({"selected_value": ""})
    assert radio_tile(options=OPTIONS, value="a", key="rt") == ""


def test_a_null_selection_is_none():
    radio_tile = _radio_tile_returning({"selected_value": None})
    assert radio_tile(options=OPTIONS, key="rt") is None


@pytest.mark.parametrize("state", [None, {}])
def test_missing_state_is_none(state):
    """No state at all (the component has not reported yet) is also None."""
    radio_tile = _radio_tile_returning(state)
    assert radio_tile(options=OPTIONS, key="rt") is None


def test_an_ordinary_selection_still_round_trips():
    radio_tile = _radio_tile_returning({"selected_value": "a"})
    assert radio_tile(options=OPTIONS, key="rt") == "a"


def test_the_stub_does_not_outlive_the_test():
    """The stub has to be invisible to whatever runs next in this process.

    Two things used to survive it. ``sys.modules["st_rsuite.radio_tile"]`` kept
    the stub-bound module, so a later test asking for the real widget silently
    got canned answers; and importing the submodule rebound it as an attribute
    of the package, shadowing the function ``st_rsuite.__getattr__`` binds
    there, so ``from st_rsuite import radio_tile`` handed out a module and
    calling it raised ``TypeError: 'module' object is not callable``.
    """
    watched = ("st_rsuite._component", "st_rsuite.radio_tile")
    before = {name: sys.modules.get(name) for name in watched}
    before_attr = st_rsuite.__dict__.get("radio_tile", _MISSING)

    _radio_tile_returning({"selected_value": "a"})

    assert {name: sys.modules.get(name) for name in watched} == before
    assert st_rsuite.__dict__.get("radio_tile", _MISSING) is before_attr
    assert not isinstance(st_rsuite.__dict__.get("radio_tile"), ModuleType)
