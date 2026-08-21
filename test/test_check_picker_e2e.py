"""e2e for check_picker (and tag_picker's new appearance param).

Covers the behavior beyond mount/roundtrip (which test_ccv2_e2e already
guards): checking an option delivers the new value to Python, grouping
renders group headings, a disabled item cannot be checked, the closed
control shows the selected count, and appearance="subtle" reaches the DOM
for both pickers.
"""

from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from e2e_utils import StreamlitRunner

pytestmark = pytest.mark.browser

ROOT_DIRECTORY = Path(__file__).parent.parent.absolute()
FIXTURE_APP = ROOT_DIRECTORY / "test" / "check_picker_e2e_app.py"


@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    with StreamlitRunner(FIXTURE_APP) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.goto(streamlit_app.server_url)
    expect(
        page.get_by_test_id("echo-ckp-subtle")
    ).to_contain_text("ckp_subtle=", timeout=60000)


def _open_check_picker(page: Page, key: str = "ckp"):
    page.locator(f".st-key-{key} .rs-picker-toggle").click()
    expect(page.locator(".rs-picker-popup").first).to_be_visible()


def test_check_picker_check_roundtrips(page: Page):
    _open_check_picker(page)
    page.locator(".rs-picker-popup").get_by_text("Vue", exact=True).click()
    expect(page.get_by_test_id("echo-ckp")).to_contain_text("react|vue")


def test_check_picker_renders_groups(page: Page):
    _open_check_picker(page)
    popup = page.locator(".rs-picker-popup")
    expect(popup.get_by_text("Frontend", exact=True)).to_be_visible()
    expect(popup.get_by_text("Backend", exact=True)).to_be_visible()


def test_check_picker_disabled_item_not_selectable(page: Page):
    _open_check_picker(page)
    page.locator(".rs-picker-popup").get_by_text("Django", exact=True).click(
        force=True
    )
    # The selection must not change; give the (non-)rerun a moment to happen.
    page.wait_for_timeout(500)
    expect(page.get_by_test_id("echo-ckp")).to_contain_text("ckp=react")


def test_check_picker_shows_count(page: Page):
    toggle = page.locator(".st-key-ckp .rs-picker-toggle")
    expect(toggle).to_contain_text("1")


def test_appearance_subtle_reaches_dom(page: Page):
    for key in ("ckp_subtle", "tp"):
        expect(
            page.locator(f".st-key-{key} [data-appearance='subtle']").first
        ).to_be_attached()
