"""Unit guard for radio_tile's return value.

``return selected if selected else None`` made a legitimately selected
``{"value": "", "label": "None of the above"}`` tile indistinguishable from no
selection at all. Only a missing selection means "nothing selected"; the empty
string is a real option value and has to survive the round trip.

The widget module is imported against a stubbed CCv2 registration because
file-backed registration only resolves inside a real ``streamlit run`` (see
test_registration_smoke).
"""

import importlib
import sys
from collections.abc import Callable
from unittest.mock import patch

import pytest

from st_rsuite import _compat

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

    for mod in ("st_rsuite._component", "st_rsuite.radio_tile"):
        sys.modules.pop(mod, None)

    with patch.object(_compat, "component", fake_registration):
        module = importlib.import_module("st_rsuite.radio_tile")
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
