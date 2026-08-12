"""RSuite Carousel component for Streamlit."""

from __future__ import annotations

import base64
import mimetypes
import os
from collections.abc import Callable
from os import PathLike

from st_rsuite._component import bind_kind

_component = bind_kind("carousel")

_MAX_LOCAL_IMAGE_BYTES = 10 * 1024 * 1024
_MAX_LOCAL_CAROUSEL_BYTES = 20 * 1024 * 1024


def _resolve_src(
    src: str | PathLike[str], *, max_bytes: int = _MAX_LOCAL_IMAGE_BYTES
) -> tuple[str, int]:
    """Resolve an explicit local path without probing ordinary URL strings.

    Returns the browser source and the number of local bytes consumed. A
    ``PathLike`` is the caller's explicit authorization to read a local asset;
    a ``str`` is always a browser reference, even when it happens to name a
    file on the server.
    """
    if isinstance(src, str):
        return src, 0
    if not isinstance(src, PathLike):
        raise TypeError("carousel item 'src' must be a string or os.PathLike")

    path = os.fspath(src)
    if not isinstance(path, str):
        raise TypeError("carousel local image paths must resolve to text")
    if max_bytes < 0:
        raise ValueError("carousel local image byte budget is exhausted")

    # Bound the read itself rather than trusting stat().st_size: pseudo-files
    # can report a misleading size, and reading one byte past the budget gives
    # a deterministic overflow check without allocating the whole file.
    with open(path, "rb") as f:
        payload = f.read(max_bytes + 1)
    if len(payload) > max_bytes:
        raise ValueError(
            f"carousel local image exceeds the {max_bytes}-byte remaining limit"
        )

    mime = mimetypes.guess_type(path)[0] or "image/jpeg"
    b64 = base64.b64encode(payload).decode()
    return f"data:{mime};base64,{b64}", len(payload)


def carousel(
    items: list[dict],
    autoplay: bool = True,
    autoplay_interval: int = 4000,
    placement: str = "bottom",
    shape: str = "dot",
    active_index: int = 0,
    locale: str | None = None,
    on_change: Callable | None = None,
    key: str | None = None,
) -> int:
    """A content/image carousel powered by RSuite.

    Parameters
    ----------
    items : list of dict
        Carousel slides. Each dict can have:
        - 'content' (str): text content to display
        - 'src' (str or os.PathLike): browser URL/data reference, or an
          explicit local path object
        - 'alt' (str): image alt text
        - 'background' (str): background color (default '#8b5cf6')
        - 'color' (str): text color (default '#fff')

        Plain strings are always passed to the browser and never probed on the
        server filesystem. To inline an app-owned local image, pass a
        ``pathlib.Path`` (or another ``os.PathLike``) chosen by the app. Local
        assets are limited to 10 MiB each and 20 MiB per carousel render; do not
        construct the path object from unsanitized user input.
    autoplay : bool
        Auto-transition between slides.
    autoplay_interval : int
        Milliseconds between auto-transitions.
    placement : str
        Indicator position: 'top', 'bottom', 'left', 'right'.
    shape : str
        Indicator shape: 'dot' or 'bar'.
    active_index : int
        Initially active slide index.
    locale : str or None
        RSuite locale key.
    on_change : callable or None
        Callback when the active slide changes.
    key : str or None
        Unique widget key.

    Returns
    -------
    int
        The active slide index.
    """

    def _noop():
        pass

    resolved_items = []
    local_bytes = 0
    for item in items:
        if "src" in item:
            remaining = min(
                _MAX_LOCAL_IMAGE_BYTES,
                _MAX_LOCAL_CAROUSEL_BYTES - local_bytes,
            )
            resolved_src, bytes_used = _resolve_src(
                item["src"], max_bytes=remaining
            )
            local_bytes += bytes_used
            resolved_items.append({**item, "src": resolved_src})
        else:
            resolved_items.append(item)

    result = _component(
        key=key,
        default={"active_index": active_index},
        data={
            "items": resolved_items,
            "autoplay": autoplay,
            "autoplayInterval": autoplay_interval,
            "placement": placement,
            "shape": shape,
            "activeIndex": active_index,
            "locale": locale,
        },
        on_active_index_change=on_change or _noop,
    )

    idx = result.get("active_index") if result else active_index
    return idx if idx is not None else active_index
