"""Callback wiring helpers shared by the multi-key (range) widgets.

CCv2 dispatches change callbacks *per state key*, not per widget: Streamlit
diffs the widget's state dict between script runs and, for every key whose value
changed, looks up ``metadata.callbacks[key]`` and runs it
(``streamlit/runtime/state/session_state.py``). A range widget writes two keys
(start and end), so registering the user's ``on_change`` on only one of them
means an edit confined to the other key never reaches the callback: extending,
shortening, or moving only the end of a range would silently skip it.

The fix is to register the same callback on both keys and dedupe, which is what
:func:`single_fire` provides.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


def single_fire(on_change: Callable[[], Any] | None) -> Callable[[], None]:
    """Wrap ``on_change`` so it runs at most once per script run.

    Register the returned callable on *every* state key the widget writes. When
    a single end of the range changes it fires once; when both ends change
    together Streamlit invokes it once per changed key, and the second
    invocation is swallowed so the user still sees exactly one call.

    The "already fired" flag lives in a closure created fresh on every widget
    render. Streamlit runs the callbacks registered by the *previous* render at
    the start of the next script run, so one closure backs exactly one callback
    phase and is inherently scoped to a single session and a single script run:
    no module-level or session-state bookkeeping is needed.

    Passing ``None`` yields a no-op, which still registers the state key with
    the runtime (and so keeps it visible in ``st.session_state``).
    """
    fired = False

    def _fire() -> None:
        nonlocal fired
        if fired:
            return
        fired = True
        if on_change is not None:
            on_change()

    return _fire
