"""e2e test for the declarative date constraints (PR 3).

Opens a constrained date_picker's calendar and asserts that min/max bounds,
explicitly disabled dates, and disabled weekdays render as non-selectable
cells, while an in-range weekday stays selectable.
"""

import re
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from e2e_utils import StreamlitRunner

ROOT_DIRECTORY = Path(__file__).parent.parent.absolute()
FIXTURE_APP = ROOT_DIRECTORY / "test" / "date_constraints_e2e_app.py"

DISABLED = re.compile(r"rs-calendar-table-cell-disabled")


@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    with StreamlitRunner(FIXTURE_APP) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.goto(streamlit_app.server_url)
    expect(page.get_by_test_id("echo-dp")).to_contain_text("2026-06-22", timeout=60000)


def _open_calendar(page: Page):
    # RSuite v6 DatePicker renders an input (aria-haspopup="dialog"); clicking it
    # opens the calendar overlay (portaled to document.body, no shadow DOM).
    page.locator(".st-key-constrained_dp .rs-input").click()
    expect(page.locator(".rs-calendar-table").first).to_be_visible()


def _cell(page: Page, day: int):
    # Same-month day cell only (adjacent-month cells repeat day numbers). The day
    # number lives in a nested .rs-calendar-table-cell-day span, matched exactly.
    return page.locator(
        ".rs-calendar-table-cell:not(.rs-calendar-table-cell-un-same-month)"
    ).filter(has=page.get_by_text(str(day), exact=True))


def test_in_range_weekday_is_enabled(page: Page):
    _open_calendar(page)
    expect(_cell(page, 22)).not_to_have_class(DISABLED)  # Mon 2026-06-22, the value
    expect(_cell(page, 19)).not_to_have_class(DISABLED)  # Fri, in range


def test_out_of_range_dates_are_disabled(page: Page):
    _open_calendar(page)
    expect(_cell(page, 10)).to_have_class(DISABLED)  # before min 2026-06-15


def test_explicitly_disabled_date_is_disabled(page: Page):
    _open_calendar(page)
    expect(_cell(page, 24)).to_have_class(DISABLED)  # in disabled_dates


def test_disabled_weekdays_are_disabled(page: Page):
    _open_calendar(page)
    expect(_cell(page, 20)).to_have_class(DISABLED)  # Saturday
    expect(_cell(page, 21)).to_have_class(DISABLED)  # Sunday
