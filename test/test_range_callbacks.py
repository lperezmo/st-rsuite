"""Regression guard for on_change dispatch on the range widgets.

CCv2 dispatches change callbacks *per state key*, not per widget: Streamlit
diffs the widget's JSON state between script runs and, for every key whose value
changed, runs ``metadata.callbacks[key]``. Each range widget writes two keys and
used to register the user's ``on_change`` on the start key only, with a no-op on
the end key, so extending, shortening, or moving only the end of a range never
reached the callback.

These tests capture the callbacks the widgets actually register and feed them to
Streamlit's own dispatcher (``SessionState._dispatch_json_change_callbacks``),
so the production dispatch path is what is under test, not a stand-in for it.

The widget modules are imported against a stubbed CCv2 registration because
file-backed registration only resolves inside a real ``streamlit run`` (see
test_registration_smoke); ``registration_stub`` owns the import and the cleanup.
"""

from collections.abc import Callable

import pytest
from registration_stub import stubbed_registration
from streamlit.runtime.state.common import WidgetMetadata
from streamlit.runtime.state.session_state import SessionState

from st_rsuite._callbacks import single_fire

# widget module/function name -> (start state key, end state key, three values)
RANGE_WIDGETS = {
    "date_range_picker": ("start_date", "end_date", "2026-06-01", "2026-06-07", "2026-06-14"),
    "date_range_input": ("start_date", "end_date", "2026-06-01", "2026-06-07", "2026-06-14"),
    "time_range_picker": ("start_time", "end_time", "09:00", "17:00", "18:30"),
}

WIDGET_NAMES = list(RANGE_WIDGETS)

requires_json_dispatch = pytest.mark.skipif(
    not hasattr(SessionState, "_dispatch_json_change_callbacks"),
    reason="this Streamlit has no per-key JSON change dispatch to drive",
)


def _register(widget: str, on_change: Callable | None) -> dict[str, Callable]:
    """Render one widget against a stubbed registration and return the callback
    map Streamlit would build from its ``on_<state key>_change`` kwargs."""
    captured: dict[str, object] = {}

    def fake_registration(name, **kwargs):
        def render(**call_kwargs):
            captured.update(call_kwargs)
            return {}

        return render

    with stubbed_registration(widget, fake_registration) as module:
        getattr(module, widget)(on_change=on_change, key="k")

    # Streamlit derives the state key from the kwarg name: on_<key>_change
    # (streamlit/components/v2/bidi_component/main.py).
    return {
        name[3:-7]: cb
        for name, cb in captured.items()
        if callable(cb) and name.startswith("on_") and name.endswith("_change")
    }


def _dispatch(callbacks: dict[str, Callable], old_map: dict, new_map: dict) -> None:
    """Run Streamlit's real per-key change dispatch over one widget's state."""
    state = SessionState()
    wid = "$$WIDGET_ID-st_rsuite_range"
    metadata = WidgetMetadata(
        id=wid,
        deserializer=lambda value, _="": value,
        serializer=lambda value: value,
        value_type="json_value",
        callbacks=callbacks,
    )
    state._new_widget_state.set_widget_metadata(metadata)
    state._new_widget_state.set_from_value(wid, new_map)
    state._old_state[wid] = old_map
    state._dispatch_json_change_callbacks(wid, metadata, (), {})


def _fire_count(widget: str, old_map: dict, new_map: dict) -> int:
    """How many times the user's on_change runs for one state transition."""
    calls: list[int] = []
    callbacks = _register(widget, lambda: calls.append(1))
    _dispatch(callbacks, old_map, new_map)
    return len(calls)


@requires_json_dispatch
@pytest.mark.parametrize("widget", WIDGET_NAMES)
def test_both_ends_changing_fires_on_change_once(widget: str):
    """Streamlit dispatches once per changed key; the user must still see one
    call."""
    start_key, end_key, a, b, c = RANGE_WIDGETS[widget]
    count = _fire_count(
        widget,
        {start_key: a, end_key: b},
        {start_key: b, end_key: c},
    )
    assert count == 1


@requires_json_dispatch
@pytest.mark.parametrize("widget", WIDGET_NAMES)
def test_only_the_end_changing_fires_on_change(widget: str):
    """The reported bug: the end key carried a no-op, so shortening or
    extending a range skipped on_change entirely."""
    start_key, end_key, a, b, c = RANGE_WIDGETS[widget]
    count = _fire_count(
        widget,
        {start_key: a, end_key: b},
        {start_key: a, end_key: c},
    )
    assert count == 1


@requires_json_dispatch
@pytest.mark.parametrize("widget", WIDGET_NAMES)
def test_only_the_start_changing_fires_on_change(widget: str):
    start_key, end_key, a, b, c = RANGE_WIDGETS[widget]
    count = _fire_count(
        widget,
        {start_key: a, end_key: c},
        {start_key: b, end_key: c},
    )
    assert count == 1


@requires_json_dispatch
@pytest.mark.parametrize("widget", WIDGET_NAMES)
def test_an_unchanged_range_does_not_fire_on_change(widget: str):
    start_key, end_key, a, b, _c = RANGE_WIDGETS[widget]
    unchanged = {start_key: a, end_key: b}
    assert _fire_count(widget, dict(unchanged), dict(unchanged)) == 0


@pytest.mark.parametrize("widget", WIDGET_NAMES)
def test_both_state_keys_carry_the_same_callable(widget: str):
    """Registering different callables on the two keys is what let one end go
    unheard; the deduping wrapper has to sit on both."""
    start_key, end_key, *_ = RANGE_WIDGETS[widget]
    callbacks = _register(widget, lambda: None)
    assert set(callbacks) == {start_key, end_key}
    assert callbacks[start_key] is callbacks[end_key]


@pytest.mark.parametrize("widget", WIDGET_NAMES)
def test_both_state_keys_are_registered_without_on_change(widget: str):
    """No on_change still registers both keys, which is what keeps them
    visible in st.session_state."""
    start_key, end_key, *_ = RANGE_WIDGETS[widget]
    callbacks = _register(widget, None)
    assert set(callbacks) == {start_key, end_key}


def test_single_fire_runs_the_callback_once_per_render():
    calls: list[int] = []
    fire = single_fire(lambda: calls.append(1))

    fire()
    fire()
    fire()

    assert calls == [1]


def test_single_fire_scopes_the_dedupe_to_one_render():
    """Each render builds a fresh closure, so the next script run fires again."""
    calls: list[int] = []

    single_fire(lambda: calls.append(1))()
    single_fire(lambda: calls.append(1))()

    assert calls == [1, 1]


def test_single_fire_without_a_callback_is_a_noop():
    fire = single_fire(None)
    fire()
    fire()
