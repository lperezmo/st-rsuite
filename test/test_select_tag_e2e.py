"""e2e for select_picker and tag_picker (PR 8).

Covers the behavior beyond mount/roundtrip (which test_ccv2_e2e already
guards): clicking an option delivers the new value to Python, grouping
renders group headings, a disabled item cannot be selected, and a creatable
tag typed by the user comes back in the return list.
"""

from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from e2e_utils import StreamlitRunner

ROOT_DIRECTORY = Path(__file__).parent.parent.absolute()
FIXTURE_APP = ROOT_DIRECTORY / "test" / "select_tag_e2e_app.py"


@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    with StreamlitRunner(FIXTURE_APP) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.goto(streamlit_app.server_url)
    expect(page.get_by_test_id("echo-tp")).to_contain_text("tp=react", timeout=60000)


def _open_select(page: Page):
    page.locator(".st-key-sp .rs-picker-toggle").click()
    expect(page.locator(".rs-picker-popup").first).to_be_visible()


def test_select_picker_click_roundtrips(page: Page):
    _open_select(page)
    page.locator(".rs-picker-popup").get_by_text("Vue", exact=True).click()
    expect(page.get_by_test_id("echo-sp")).to_contain_text("sp=vue")


def test_select_picker_renders_groups(page: Page):
    _open_select(page)
    popup = page.locator(".rs-picker-popup")
    expect(popup.get_by_text("Frontend", exact=True)).to_be_visible()
    expect(popup.get_by_text("Backend", exact=True)).to_be_visible()


def test_select_picker_disabled_item_not_selectable(page: Page):
    _open_select(page)
    page.locator(".rs-picker-popup").get_by_text("Django", exact=True).click(force=True)
    # The selection must not change; give the (non-)rerun a moment to happen.
    page.wait_for_timeout(500)
    expect(page.get_by_test_id("echo-sp")).to_contain_text("sp=react")


def test_tag_picker_creatable_roundtrips(page: Page):
    tag_input = page.locator(".st-key-tp .rs-picker-search-input input")
    tag_input.click()
    tag_input.fill("svelte")
    # RSuite shows a "Create option" entry for unknown values; click it.
    page.locator(".rs-picker-popup").get_by_text("svelte").click()
    expect(page.get_by_test_id("echo-tp")).to_contain_text("svelte")
