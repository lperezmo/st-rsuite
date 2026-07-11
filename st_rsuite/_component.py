"""Single shared CCv2 registration for every st-rsuite widget.

All widgets ship in one frontend bundle (one asset_dir, one network fetch,
one cached copy of React/RSuite per page). The bundle's entry routes on a
``kind`` discriminator in ``data``; each widget module binds its own kind via
:func:`bind_kind` and keeps its public Python API unchanged.
"""

from __future__ import annotations

from typing import Any, Callable

from st_rsuite._compat import component

_rsuite = component(
    "st-rsuite.rsuite",
    js="index-*.js",
    html='<div class="react-root"></div>',
)


def bind_kind(kind: str) -> Callable[..., Any]:
    """Return a renderer for one widget kind.

    The returned callable accepts the same keyword arguments as the object
    returned by ``st.components.v2.component`` and injects ``kind`` into
    ``data`` so the frontend dispatches to the right React component.
    """

    def render(*, data: dict[str, Any], **kwargs: Any) -> Any:
        return _rsuite(data={"kind": kind, **data}, **kwargs)

    return render
