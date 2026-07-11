"""CCv2 e2e tests for st-rsuite.

These run a real Streamlit server and drive it with Playwright. Each component
mounts a Components-v2 node at `.st-key-<key> .stBidiComponent` (no iframe), and
RSuite renders `rs-*` elements inside it. The fixture app echoes each return
value so we can assert the Python <-> JS round-trip.

This is the authoritative regression guard for the reporter's bug
(`Component 'st-rsuite.rsuite' must be declared ... with asset_dir`): if the
shared component fails to register on a given Streamlit version, nothing
mounts here.
"""

from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from e2e_utils import StreamlitRunner

ROOT_DIRECTORY = Path(__file__).parent.parent.absolute()
FIXTURE_APP = ROOT_DIRECTORY / "test" / "ccv2_e2e_app.py"

ALL_KEYS = [
    "date_picker",
    "date_range_picker",
    "time_picker",
    "time_range_picker",
    "date_input",
    "date_range_input",
    "radio_tile",
    "select_picker",
    "tag_picker",
    "check_tree",
    "check_tree_picker",
    "tree_picker",
    "cascader",
    "multi_cascade_tree",
    "carousel",
    "timeline",
    "pin_input",
]

# key -> substring expected in that component's echoed return value
ROUNDTRIPS = {
    "date_picker": "2026-06-22",
    "date_range_picker": "2026-06-22|2026-06-29",
    "time_picker": "09:30",
    "time_range_picker": "09:00",
    "date_input": "2026-06-22",
    "date_range_input": "2026-06-22|2026-06-29",
    "radio_tile": "rt=a",
    "select_picker": "sp=react",
    "tag_picker": "react|vue",
    "check_tree": "react",
    "check_tree_picker": "react",
    "tree_picker": "tpv=react",
    "cascader": "cas=sf",
    "multi_cascade_tree": "sf",
    "carousel": "car=0",
    "pin_input": "123456",
}


@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    with StreamlitRunner(FIXTURE_APP) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.goto(streamlit_app.server_url)
    # Wait for the whole first script run to finish: the LAST component renders
    # and echoes its value. All 17 widgets share one bundle, but the first
    # render still takes a while; asserting earlier races the render.
    expect(page.get_by_test_id("echo-pin_input")).to_contain_text("123456", timeout=60000)
    expect(page.locator(".st-key-pin_input .stBidiComponent")).to_be_attached()


def _comp(page: Page, key: str):
    return page.locator(f".st-key-{key} .stBidiComponent")


def test_all_components_mount(page: Page):
    """Every component registers and mounts a CCv2 node (and never an iframe)."""
    for key in ALL_KEYS:
        expect(_comp(page, key)).to_be_attached()
        expect(page.locator(f".st-key-{key} iframe")).to_have_count(0)


def test_all_components_render_rsuite(page: Page):
    """Each mounted component actually renders RSuite markup, not an empty shell."""
    for key in ALL_KEYS:
        expect(_comp(page, key).locator("[class*='rs-']").first).to_be_visible()


@pytest.mark.parametrize("key,expected", list(ROUNDTRIPS.items()))
def test_value_roundtrip(page: Page, key: str, expected: str):
    """The default value round-trips from Python to the frontend and back."""
    expect(page.get_by_test_id(f"echo-{key}")).to_contain_text(expected)


def test_radio_tile_selection_roundtrip(page: Page):
    """Clicking a tile reruns the script and delivers the new value to Python."""
    tile = _comp(page, "radio_tile")
    expect(tile.locator("[class*='rs-']").first).to_be_visible()
    expect(page.get_by_test_id("echo-radio_tile")).to_contain_text("rt=a")

    tile.get_by_text("Option B").click()
    expect(page.get_by_test_id("echo-radio_tile")).to_contain_text("rt=b")
