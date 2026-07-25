"""Import a widget module against a stubbed CCv2 registration, then put the
interpreter back the way it was.

File-backed registration only resolves inside a real ``streamlit run`` (see
test_registration_smoke), so unit tests that need to see what a widget passes to
the component have to re-import it with ``_compat.component`` patched. Doing
that by hand leaks in two places, and both outlive the test:

- ``sys.modules["st_rsuite.<widget>"]`` keeps the stub-bound module, whose
  ``_component`` is a closure over a patch that no longer exists;
- importing a submodule rebinds it as an attribute of the parent package,
  overwriting the function that ``st_rsuite.__getattr__`` bound there. After
  that, ``from st_rsuite import radio_tile`` hands out the *module*, and calling
  it raises ``TypeError: 'module' object is not callable``.

Nothing caught this while each of these files was a CI job of its own. The
version matrix now runs ``pytest test/``, one process for the whole suite, so a
later test that imports a stubbed widget normally would collect the wreckage.
"""

from __future__ import annotations

import importlib
import sys
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from types import ModuleType
from unittest.mock import patch

from st_rsuite import _compat

# Every widget module imports bind_kind from here, so the shared registration
# has to be reloaded too or the stub never reaches the widget.
_SHARED = "st_rsuite._component"


@contextmanager
def stubbed_registration(
    widget: str, factory: Callable[..., Callable]
) -> Iterator[ModuleType]:
    """Yield ``st_rsuite.<widget>`` imported with ``factory`` standing in for
    ``st.components.v2.component``.

    The yielded module (and anything taken from it) stays bound to the stub
    after the block exits, which is what makes it usable in a test; what gets
    restored is the interpreter's view of the package, so the *next* import of
    the widget is the real one.
    """
    module_name = f"st_rsuite.{widget}"
    names = (_SHARED, module_name)
    saved_modules = {name: sys.modules.get(name) for name in names}

    package = sys.modules["st_rsuite"]
    missing = object()
    saved_attr = package.__dict__.get(widget, missing)

    for name in names:
        sys.modules.pop(name, None)

    try:
        with patch.object(_compat, "component", factory):
            yield importlib.import_module(module_name)
    finally:
        for name, module in saved_modules.items():
            if module is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module

        if saved_attr is missing:
            package.__dict__.pop(widget, None)
        else:
            setattr(package, widget, saved_attr)
