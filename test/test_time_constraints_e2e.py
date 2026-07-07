"""e2e test for time constraints (PR 4).

Opens a business-hours time_picker and asserts the hour column hides hours
outside the [min_hour, max_hour] window while keeping in-window hours.
"""

from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from e2e_utils import StreamlitRunner

ROOT_DIRECTORY = Path(__file__).parent.parent.absolute()
FIXTURE_APP = ROOT_DIRECTORY / "test" / "time_constraints_e2e_app.py"


@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    with StreamlitRunner(FIXTURE_APP) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.goto(streamlit_app.server_url)
    expect(page.get_by_test_id("echo-tp")).to_contain_text("09:00", timeout=60000)


def _hours_column(page: Page):
    page.locator(".st-key-business_tp .rs-input").click()
    expect(page.locator(".rs-calendar-time-dropdown-column").first).to_be_visible()
    # The first dropdown column is hours; minutes follow in later columns.
    return page.locator(".rs-calendar-time-dropdown-column").first


def test_in_window_hours_present(page: Page):
    hours = _hours_column(page)
    expect(hours.get_by_text("09", exact=True)).to_be_visible()
    expect(hours.get_by_text("17", exact=True)).to_be_visible()


def test_out_of_window_hours_hidden(page: Page):
    hours = _hours_column(page)
    expect(hours.get_by_text("07", exact=True)).to_have_count(0)  # before min_hour
    expect(hours.get_by_text("20", exact=True)).to_have_count(0)  # after max_hour
