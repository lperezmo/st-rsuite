"""e2e for cascader and tree_picker (PR 9).

Covers behavior beyond mount/roundtrip (which test_ccv2_e2e already guards):
navigating cascade columns to a leaf delivers the value to Python, and the
tree picker's only_leaf_selectable keeps branch nodes unselectable while a
leaf click round-trips.
"""

from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from e2e_utils import StreamlitRunner

ROOT_DIRECTORY = Path(__file__).parent.parent.absolute()
FIXTURE_APP = ROOT_DIRECTORY / "test" / "cascader_tree_e2e_app.py"


@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    with StreamlitRunner(FIXTURE_APP) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.goto(streamlit_app.server_url)
    expect(page.get_by_test_id("echo-tpv")).to_contain_text("tpv=None", timeout=60000)


def test_cascader_column_navigation_roundtrips(page: Page):
    page.locator(".st-key-cas .rs-picker-toggle").click()
    popup = page.locator(".rs-picker-popup")
    expect(popup).to_be_visible()
    popup.get_by_text("United States", exact=True).click()
    popup.get_by_text("California", exact=True).click()
    popup.get_by_text("San Francisco", exact=True).click()
    expect(page.get_by_test_id("echo-cas")).to_contain_text("cas=sf")


def test_tree_picker_leaf_selection_roundtrips(page: Page):
    page.locator(".st-key-tpv .rs-picker-toggle").click()
    popup = page.locator(".rs-picker-popup")
    expect(popup).to_be_visible()
    popup.get_by_text("Vue", exact=True).click()
    expect(page.get_by_test_id("echo-tpv")).to_contain_text("tpv=vue")


def test_tree_picker_branch_not_selectable(page: Page):
    page.locator(".st-key-tpv .rs-picker-toggle").click()
    popup = page.locator(".rs-picker-popup")
    expect(popup).to_be_visible()
    popup.get_by_text("Backend", exact=True).click()
    # only_leaf_selectable: clicking a branch must not change the selection.
    page.wait_for_timeout(500)
    expect(page.get_by_test_id("echo-tpv")).to_contain_text("tpv=None")
