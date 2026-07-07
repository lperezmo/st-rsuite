"""e2e test for custom DateRangePicker shortcut presets (PR 5).

Opens the overlay, clicks a custom preset, and asserts it selects the range the
Python side declared.
"""

from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from e2e_utils import StreamlitRunner

ROOT_DIRECTORY = Path(__file__).parent.parent.absolute()
FIXTURE_APP = ROOT_DIRECTORY / "test" / "range_shortcuts_e2e_app.py"


@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    with StreamlitRunner(FIXTURE_APP) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.goto(streamlit_app.server_url)
    expect(page.get_by_test_id("echo-drp")).to_contain_text("drp=", timeout=60000)


def _open_overlay(page: Page):
    page.locator(".st-key-preset_drp .rs-input").first.click()
    expect(page.locator(".rs-picker-toolbar-ranges").first).to_be_visible()


def test_custom_presets_render(page: Page):
    _open_overlay(page)
    ranges = page.locator(".rs-picker-toolbar-ranges")
    expect(ranges.get_by_role("button", name="June week")).to_be_visible()
    expect(ranges.get_by_role("button", name="Single day")).to_be_visible()


def test_clicking_preset_selects_its_range(page: Page):
    _open_overlay(page)
    page.get_by_role("button", name="June week").click()
    # The preset declared (2026-06-15, 2026-06-21); it must round-trip to Python.
    expect(page.get_by_test_id("echo-drp")).to_contain_text("2026-06-15|2026-06-21")
