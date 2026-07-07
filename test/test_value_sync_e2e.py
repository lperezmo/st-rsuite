"""e2e regression guard for two-way value sync.

Before the useSyncedValue fix, every component seeded local React state once and
ignored later Python-side `value=` changes. These tests change `value=` at
runtime (via a Streamlit button) and assert the widget adopts it, and that a
user edit still round-trips back to Python.
"""

from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from e2e_utils import StreamlitRunner

ROOT_DIRECTORY = Path(__file__).parent.parent.absolute()
FIXTURE_APP = ROOT_DIRECTORY / "test" / "value_sync_e2e_app.py"


@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    with StreamlitRunner(FIXTURE_APP) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.goto(streamlit_app.server_url)
    # Wait for the first full render: both bundles load before the echoes appear.
    expect(page.get_by_test_id("echo-ct")).to_contain_text("react", timeout=60000)
    expect(page.locator(".st-key-synced_dp .stBidiComponent")).to_be_attached()


def _comp(page: Page, key: str):
    return page.locator(f".st-key-{key} .stBidiComponent")


def test_python_value_change_updates_date_picker(page: Page):
    """Changing value= from Python updates the mounted picker's display."""
    date_input = _comp(page, "synced_dp").locator("input").first
    expect(date_input).to_have_value("2026-06-22")

    page.get_by_role("button", name="set date").click()

    # Would stay "2026-06-22" before the fix (initial-only hydration).
    expect(date_input).to_have_value("2030-01-01")


def test_python_value_change_updates_check_tree(page: Page):
    """Changing value= from Python re-checks the tree to match."""
    tree = _comp(page, "synced_ct")
    expect(tree.get_by_role("checkbox", name="React")).to_be_checked()
    expect(tree.get_by_role("checkbox", name="Vue")).not_to_be_checked()

    page.get_by_role("button", name="set tree").click()

    expect(tree.get_by_role("checkbox", name="Vue")).to_be_checked()
    expect(tree.get_by_role("checkbox", name="React")).not_to_be_checked()


def test_user_edit_still_roundtrips(page: Page):
    """A user edit reaches Python and is not reverted by the value= echo."""
    tree = _comp(page, "synced_ct")
    expect(page.get_by_test_id("echo-ct")).to_contain_text("['react']")

    tree.get_by_text("Vue", exact=True).click()

    # With cascade off, checking Vue adds it alongside React. The selection must
    # persist across the rerun the click triggers, rather than being reverted by
    # the static value= (the echo-fighting regression).
    expect(page.get_by_test_id("echo-ct")).to_contain_text("['react', 'vue']")
    expect(tree.get_by_role("checkbox", name="Vue")).to_be_checked()
