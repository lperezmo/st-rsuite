"""e2e test for popup anchoring while Streamlit's main section scrolls.

RSuite portals picker popups to document.body and positions them once; it only
re-anchors on window resize and popup resize, never on the scrolling Streamlit
actually does inside `section[data-testid="stMain"]`. `useAnchoredPopup` (frontend/src/shared)
tracks the toggle on every scroll frame, flips the popup above the toggle
when it no longer fits below, and hides it once the toggle leaves the view.
"""

from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from e2e_utils import StreamlitRunner

pytestmark = pytest.mark.browser

ROOT_DIRECTORY = Path(__file__).parent.parent.absolute()
FIXTURE_APP = ROOT_DIRECTORY / "test" / "popup_anchoring_e2e_app.py"

MAIN = '[data-testid="stMain"]'
POPUP = ".rs-picker-popup"

# Playwright's default viewport is 1280x720; every scroll target below assumes
# that height, so pin it rather than inherit whatever the runner configures.
VIEWPORT = {"width": 1280, "height": 720}


@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    with StreamlitRunner(FIXTURE_APP) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.set_viewport_size(VIEWPORT)
    page.goto(streamlit_app.server_url)
    expect(page.get_by_test_id("echo-dp")).to_contain_text("2026-06-22", timeout=60000)


def _scroll_main(page: Page, top: int) -> None:
    """Scroll Streamlit's main section and wait one frame for the popup."""
    page.evaluate(
        "([sel, top]) => { document.querySelector(sel).scrollTop = top; }",
        [MAIN, top],
    )
    # The hook repositions on requestAnimationFrame after the scroll event.
    page.wait_for_timeout(150)


def _scroll_toggle_to(page: Page, toggle_selector: str, viewport_top: float) -> None:
    """Scroll the main section so `toggle_selector` sits at `viewport_top`."""
    page.evaluate(
        """([mainSel, sel, want]) => {
            const main = document.querySelector(mainSel);
            const rect = document.querySelector(sel).getBoundingClientRect();
            main.scrollTop += rect.top - want;
        }""",
        [MAIN, toggle_selector, viewport_top],
    )
    page.wait_for_timeout(150)


def _rect(page: Page, selector: str) -> dict:
    return page.evaluate(
        "sel => document.querySelector(sel).getBoundingClientRect().toJSON()",
        selector,
    )


def _settled_popup(page: Page, **expected) -> dict:
    """Poll until the popup matches `expected` (placement, visibility), then
    return its state. Repositioning happens on the next animation frame after
    a scroll, so a single immediate read would race it."""
    deadline = 3000
    state = _popup_state(page)
    while deadline > 0 and any(state[k] != v for k, v in expected.items()):
        page.wait_for_timeout(50)
        deadline -= 50
        state = _popup_state(page)
    for k, v in expected.items():
        assert state[k] == v, f"{k}={state[k]!r}, expected {v!r}: {state}"
    return state


def _popup_state(page: Page) -> dict:
    return page.evaluate(
        """sel => {
            const el = document.querySelector(sel);
            const r = el.getBoundingClientRect();
            return {
                top: r.top, bottom: r.bottom, left: r.left, height: r.height,
                placement: el.dataset.placement,
                visibility: el.style.visibility,
            };
        }""",
        POPUP,
    )


def test_popup_follows_toggle_while_main_scrolls(page: Page):
    toggle = ".st-key-anchored_dp .rs-picker"
    page.locator(f"{toggle} .rs-input").click()
    expect(page.locator(".rs-calendar-table").first).to_be_visible()

    popup = _settled_popup(page, placement="bottom-start", visibility="")
    anchor = _rect(page, toggle)
    assert abs(popup["top"] - anchor["bottom"]) < 2
    assert abs(popup["left"] - anchor["left"]) < 2

    _scroll_main(page, 120)
    moved = _rect(page, toggle)
    assert moved["top"] < anchor["top"] - 100, "fixture must actually scroll"
    popup = _settled_popup(page, visibility="")
    assert abs(popup["top"] - moved["bottom"]) < 2, "popup did not follow its toggle"


def test_popup_hides_when_toggle_scrolls_out_of_view_and_returns(page: Page):
    toggle = ".st-key-anchored_dp .rs-picker"
    page.locator(f"{toggle} .rs-input").click()
    expect(page.locator(".rs-calendar-table").first).to_be_visible()

    _scroll_main(page, 2000)
    assert _rect(page, toggle)["bottom"] < 0, "toggle should be above the viewport"
    popup = _settled_popup(page, visibility="hidden")
    # Parked inside the viewport so it cannot extend the document.
    assert popup["top"] >= 0 and popup["bottom"] <= VIEWPORT["height"] + 1

    _scroll_main(page, 0)
    popup = _settled_popup(page, visibility="")
    anchor = _rect(page, toggle)
    assert abs(popup["top"] - anchor["bottom"]) < 2


def test_popup_flips_above_toggle_near_bottom_edge_and_back(page: Page):
    toggle = ".st-key-lower_sp .rs-picker"
    # The lower picker mounts below the fold, after the echo the fixture waits on.
    expect(page.locator(toggle)).to_be_attached(timeout=30000)
    # Put the toggle 80px above the bottom edge: the menu cannot fit below.
    _scroll_toggle_to(page, toggle, VIEWPORT["height"] - 80)
    page.locator(f"{toggle} .rs-picker-toggle").click()
    expect(page.locator(POPUP)).to_be_visible()

    popup = _settled_popup(page, placement="top-start")
    anchor = _rect(page, toggle)
    assert popup["height"] > 80, "menu must be taller than the room below"
    assert abs(popup["bottom"] - anchor["top"]) < 2

    # Scroll so the toggle sits mid-screen with room below: flips back.
    _scroll_toggle_to(page, toggle, 200)
    popup = _settled_popup(page, placement="bottom-start")
    anchor = _rect(page, toggle)
    assert abs(popup["top"] - anchor["bottom"]) < 2

    # And forward again once the room below is gone.
    _scroll_toggle_to(page, toggle, VIEWPORT["height"] - 80)
    popup = _settled_popup(page, placement="top-start")
    anchor = _rect(page, toggle)
    assert abs(popup["bottom"] - anchor["top"]) < 2
