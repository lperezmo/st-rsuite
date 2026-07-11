"""Single-bundle e2e: the architectural guarantees of the shared bundle.

A page mixing several widget kinds must fetch the st-rsuite entry bundle
exactly once (the whole point of the single-bundle architecture), and the
lazy locale chunks must actually load from Streamlit's component asset route
(the riskiest part of the refactor: code-split chunks resolve relative to the
entry module's URL).
"""

import fnmatch
from pathlib import Path
from urllib.parse import urlparse

import pytest
from playwright.sync_api import Page, expect

from e2e_utils import StreamlitRunner

ROOT_DIRECTORY = Path(__file__).parent.parent.absolute()
FIXTURE_APP = ROOT_DIRECTORY / "test" / "single_bundle_e2e_app.py"

WIDGET_KEYS = [
    "date_picker",
    "time_picker",
    "check_tree",
    "date_picker_ja",
    "pin_input",
]


@pytest.fixture(scope="module")
def streamlit_app():
    with StreamlitRunner(FIXTURE_APP) as runner:
        yield runner


@pytest.fixture
def rsuite_requests(page: Page, streamlit_app: StreamlitRunner):
    """Collect requests to the st-rsuite component asset route, then load
    the app and wait for the first script run to finish."""
    requests: list[str] = []
    page.on(
        "request",
        lambda request: "st-rsuite" in request.url and requests.append(request.url),
    )
    page.goto(streamlit_app.server_url)
    expect(page.get_by_test_id("echo-pin_input")).to_contain_text(
        "pin=123456", timeout=60000
    )
    for key in WIDGET_KEYS:
        expect(page.locator(f".st-key-{key} .stBidiComponent")).to_be_attached()
    return requests


def test_one_bundle_fetch_for_many_widgets(page: Page, rsuite_requests: list[str]):
    """Five widgets across four kinds share ONE entry-bundle fetch."""
    entry_fetches = [
        url
        for url in rsuite_requests
        if fnmatch.fnmatch(Path(urlparse(url).path).name, "index-*.js")
    ]
    assert len(entry_fetches) == 1, (
        f"expected exactly one entry bundle fetch, saw {entry_fetches}"
    )


def test_locale_chunk_loads_and_localizes(page: Page, rsuite_requests: list[str]):
    """The ja_JP widget pulls its lazy locale chunk over the component asset
    route and the calendar actually renders localized weekday names."""
    # Open the localized picker: the calendar header must show Japanese
    # weekday abbreviations. This only renders once the chunk has executed,
    # so it also synchronizes the request-log assertion below (the chunk
    # fetch is async and may land after the fixture's initial waits).
    page.locator(".st-key-date_picker_ja .rs-input").click()
    expect(page.locator(".rs-calendar-table-header-row").first).to_contain_text(
        "日", timeout=10000
    )

    locale_fetches = [
        url
        for url in rsuite_requests
        if fnmatch.fnmatch(Path(urlparse(url).path).name, "chunk-ja_JP-*.js")
    ]
    assert len(locale_fetches) == 1, (
        f"expected exactly one ja_JP locale chunk fetch, saw {locale_fetches}"
    )
