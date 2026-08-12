"""Security guards for carousel browser and local image sources."""

from __future__ import annotations

import base64
from collections.abc import Callable
from pathlib import Path

import pytest
from registration_stub import stubbed_registration


def _carousel_module(factory: Callable):
    with stubbed_registration("carousel", factory) as module:
        return module


def _unused_registration(name, **kwargs):
    def render(**call_kwargs):
        return {"active_index": 0}

    return render


def test_plain_string_that_names_a_file_is_never_read(tmp_path: Path):
    secret = tmp_path / "secret.txt"
    secret.write_text("server-secret")
    module = _carousel_module(_unused_registration)

    resolved, bytes_used = module._resolve_src(str(secret))

    assert resolved == str(secret)
    assert bytes_used == 0
    assert "server-secret" not in resolved


def test_relative_and_home_path_strings_are_browser_references(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    secret = tmp_path / "secret.png"
    secret.write_bytes(b"server-secret")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path))
    module = _carousel_module(_unused_registration)

    for source in ("secret.png", "~/secret.png"):
        assert module._resolve_src(source) == (source, 0)


@pytest.mark.parametrize(
    "source",
    [
        "https://example.com/image.png",
        "data:image/png;base64,AA==",
        "./browser-relative/image.png",
    ],
)
def test_browser_string_sources_are_unchanged(source: str):
    module = _carousel_module(_unused_registration)
    assert module._resolve_src(source) == (source, 0)


def test_explicit_path_is_inlined_with_a_bounded_read(tmp_path: Path):
    image = tmp_path / "pixel.png"
    payload = b"not-a-real-png-but-explicit-app-owned-bytes"
    image.write_bytes(payload)
    module = _carousel_module(_unused_registration)

    resolved, bytes_used = module._resolve_src(image, max_bytes=len(payload))

    assert bytes_used == len(payload)
    assert resolved == (
        "data:image/png;base64," + base64.b64encode(payload).decode()
    )


def test_explicit_path_over_the_read_limit_is_rejected(tmp_path: Path):
    image = tmp_path / "large.png"
    image.write_bytes(b"12345")
    module = _carousel_module(_unused_registration)

    with pytest.raises(ValueError, match="exceeds the 4-byte remaining limit"):
        module._resolve_src(image, max_bytes=4)


def test_carousel_enforces_an_aggregate_local_byte_budget(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    first = tmp_path / "first.png"
    second = tmp_path / "second.png"
    first.write_bytes(b"123")
    second.write_bytes(b"456")
    module = _carousel_module(_unused_registration)
    monkeypatch.setattr(module, "_MAX_LOCAL_IMAGE_BYTES", 5)
    monkeypatch.setattr(module, "_MAX_LOCAL_CAROUSEL_BYTES", 5)

    with pytest.raises(ValueError, match="exceeds the 2-byte remaining limit"):
        module.carousel(items=[{"src": first}, {"src": second}], autoplay=False)
