"""e2e test for label/control accessibility (PR 6).

Every labeled date/time component must associate its <label> to the control via
htmlFor -> id (previously missing), and render the help tooltip.
"""

from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from e2e_utils import StreamlitRunner

ROOT_DIRECTORY = Path(__file__).parent.parent.absolute()
FIXTURE_APP = ROOT_DIRECTORY / "test" / "a11y_e2e_app.py"

# key -> help text passed in the fixture
LABELED = {
    "dp": "dp help",
    "drp": "drp help",
    "tp": "tp help",
    "trp": "trp help",
    "di": "di help",
    "dri": "dri help",
}


@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    with StreamlitRunner(FIXTURE_APP) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.goto(streamlit_app.server_url)
    expect(page.get_by_test_id("ready")).to_contain_text("ready", timeout=60000)


@pytest.mark.parametrize("key", list(LABELED))
def test_label_is_associated_to_a_control(page: Page, key: str):
    comp = page.locator(f".st-key-{key}")
    label = comp.locator("label")
    for_attr = label.get_attribute("for")
    assert for_attr, f"{key}: label has no htmlFor"
    # An element with that id must exist inside the component (the control).
    expect(comp.locator(f"#{for_attr.replace(':', chr(92) + ':')}")).to_have_count(1)


@pytest.mark.parametrize("key,help_text", list(LABELED.items()))
def test_help_tooltip_present(page: Page, key: str, help_text: str):
    marker = page.locator(f".st-key-{key} label span[title]")
    expect(marker).to_have_attribute("title", help_text)
