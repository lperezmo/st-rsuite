"""e2e regression guards for the reviewed defects that live in the browser.

Each test pins one fix that only shows up against a real Streamlit server and a
real RSuite render:

- ``datetime`` defaults reach the date fields as dates, not timestamps,
- a disabled tree is disabled for the keyboard too, not just the mouse,
- distinct word splits keep distinct value-sync keys,
- the RSuite theme re-detects when Streamlit's appearance changes.

The PinInput controlled/uncontrolled fix has no test here on purpose: with
RSuite's useControlled, ``value={pinValue || undefined}`` and
``value={pinValue}`` are observationally identical from the browser, so any
test written against it would pass on the unfixed code too.
"""

import re
from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from e2e_utils import StreamlitRunner

ROOT_DIRECTORY = Path(__file__).parent.parent.absolute()
FIXTURE_APP = ROOT_DIRECTORY / "test" / "review_findings_e2e_app.py"

# Focusable by the tab key. Nodes with tabindex="-1" are deliberately excluded:
# they are already out of the tab order without any help from the fix.
TABBABLE = 'input:not([type="hidden"]), a[href], button, [tabindex]:not([tabindex="-1"])'


@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    with StreamlitRunner(FIXTURE_APP) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.goto(streamlit_app.server_url)
    expect(page.get_by_test_id("ready")).to_contain_text("ready", timeout=60000)
    # The last component having painted RSuite markup means the shared bundle
    # loaded and every widget on the page mounted.
    expect(
        page.locator(".st-key-themed_dp .stBidiComponent [class*='rs-']").first
    ).to_be_visible(timeout=60000)


def _comp(page: Page, key: str):
    return page.locator(f".st-key-{key} .stBidiComponent")


def _fields(page: Page, key: str):
    return _comp(page, key).locator('input:not([type="hidden"])')


# -- datetime defaults -------------------------------------------------------


def test_date_input_renders_a_datetime_default(page: Page):
    """A datetime default used to serialize to a full timestamp, which the
    field could not parse, so it rendered empty and came back as None."""
    expect(_fields(page, "dt_di").first).to_have_value("2026-06-22")
    expect(page.get_by_test_id("echo-dt_di")).to_have_text("di=2026-06-22")


def test_date_range_input_renders_datetime_defaults(page: Page):
    expect(_fields(page, "dt_dri").first).to_have_value("2026-06-22 ~ 2026-06-29")
    expect(page.get_by_test_id("echo-dt_dri")).to_have_text(
        "dri=2026-06-22|2026-06-29"
    )


# -- disabled trees ----------------------------------------------------------


@pytest.mark.parametrize(
    "key,expected",
    [("disabled_ct", "ct=['react']"), ("disabled_mct", "mct=['sf']")],
)
def test_disabled_tree_refuses_focus_and_keeps_its_value(
    page: Page, key: str, expected: str
):
    """pointerEvents blocked the mouse only, so a keyboard user could focus a
    checkbox inside a "disabled" tree and toggle it straight back to Python."""
    echo = page.get_by_test_id(f"echo-{key}")
    expect(echo).to_have_text(expected)

    focus_probe = _comp(page, key).evaluate(
        """(el, selector) => {
            const nodes = [...el.querySelectorAll(selector)];
            const reached = [];
            for (const node of nodes) {
                node.focus();
                if (el.contains(document.activeElement)) reached.push(node.outerHTML);
            }
            return { count: nodes.length, reached };
        }""",
        TABBABLE,
    )

    # Guard against a vacuous pass: the tree must contain controls that would
    # be focusable if nothing stopped them.
    assert focus_probe["count"] > 0, f"{key} rendered no focusable controls"
    assert focus_probe["reached"] == [], f"{key} let focus inside: {focus_probe['reached']}"

    page.keyboard.press("Space")
    expect(echo).to_have_text(expected)


def test_tab_order_skips_the_disabled_trees(page: Page):
    """Walk the tab order across both disabled trees; focus must never land
    inside either one."""
    _fields(page, "dt_dri").first.focus()

    inside = []
    for _ in range(12):
        page.keyboard.press("Tab")
        inside.append(
            page.evaluate(
                """() => {
                    const el = document.activeElement;
                    if (!el || !el.closest) return null;
                    const owner = el.closest(
                        '.st-key-disabled_ct, .st-key-disabled_mct'
                    );
                    return owner ? owner.className : null;
                }"""
            )
        )

    assert [entry for entry in inside if entry] == []


# -- value-sync key ----------------------------------------------------------


def test_distinct_word_splits_stay_distinct(page: Page):
    """["New York"] and ["New", "York"] must produce different sync keys, or a
    Python-driven change between them looks like no change at all and the
    widget ignores it. This is why keyOfList joins on NUL and not on a space."""
    tags = _comp(page, "collide_tp").locator(".rs-tag")
    expect(tags).to_have_count(1)
    expect(tags.first).to_contain_text("New York")

    page.get_by_role("button", name="split tags").click()

    expect(tags).to_have_count(2)


# -- theme re-detection ------------------------------------------------------


_STREAMLIT_BACKGROUND = """() => {
    const root = document.querySelector('.st-key-themed_dp .react-root');
    if (!root) return '';
    return getComputedStyle(root)
        .getPropertyValue('--st-background-color')
        .trim()
        .toLowerCase();
}"""


def test_rsuite_theme_follows_a_streamlit_appearance_change(page: Page):
    """The theme was read from documentElement, where Streamlit never puts its
    --st-* vars, and the empty result was cached for the life of the page: a
    flip to dark left RSuite popups light-on-dark until a hard refresh."""
    body = page.locator("body")
    expect(body).to_have_class(re.compile(r"rs-theme-light"))

    light_background = page.evaluate(_STREAMLIT_BACKGROUND)
    assert light_background, "Streamlit did not expose --st-background-color"

    page.emulate_media(color_scheme="dark")
    # Streamlit itself has to switch first, or the assertion below proves
    # nothing about the bridge.
    page.wait_for_function(
        f"previous => ({_STREAMLIT_BACKGROUND})() !== previous",
        arg=light_background,
        timeout=30000,
    )

    # Re-render the picker so the bridge has to resolve the appearance again.
    page.get_by_role("button", name="rerender").click()
    expect(page.locator(".st-key-themed_dp label")).to_contain_text("render 1")

    expect(body).to_have_class(re.compile(r"rs-theme-dark"))
