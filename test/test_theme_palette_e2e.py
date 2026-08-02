"""e2e guard for RSuite's accent color following Streamlit's primary color.

RSuite ships a fixed blue primary ramp, and nothing pointed it at
``--st-primary-color``. A themed app therefore drew its own widgets in one color
and its st-rsuite widgets in RSuite's blue. This repo's own fixture theme is
violet (see .streamlit/config.toml), which is what makes the mismatch visible
here without any extra setup.
"""

from pathlib import Path

import pytest
from playwright.sync_api import Page, expect

from e2e_utils import StreamlitRunner

pytestmark = pytest.mark.browser

ROOT_DIRECTORY = Path(__file__).parent.parent.absolute()
FIXTURE_APP = ROOT_DIRECTORY / "test" / "ccv2_e2e_app.py"

# The stock RSuite primary. Any assertion below that comes back as this color
# means the bridge did not run at all.
RSUITE_STOCK_PRIMARY = "#3498ff"


@pytest.fixture(autouse=True, scope="module")
def streamlit_app():
    with StreamlitRunner(FIXTURE_APP) as runner:
        yield runner


@pytest.fixture(autouse=True, scope="function")
def go_to_app(page: Page, streamlit_app: StreamlitRunner):
    page.goto(streamlit_app.server_url)
    # Wait for painted RSuite markup, not merely for the component container.
    # The container is attached as soon as Streamlit writes the element, which
    # is before the bundle has been fetched and the renderer has run, and the
    # palette is written by that renderer. Gating on the container alone reads
    # the ramp too early and fails against correct code. Rendered markup is a
    # sound gate because the renderer applies the palette before it mounts the
    # React tree.
    expect(page.locator(".st-key-date_picker input").first).to_be_visible(
        timeout=60_000
    )


def _hex_to_rgb_string(value: str) -> str:
    """'#7c3aed' -> 'rgb(124, 58, 237)', which is what getComputedStyle returns."""
    raw = value.lstrip("#")
    red, green, blue = (int(raw[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgb({red}, {green}, {blue})"


def _configured_primary(page: Page) -> str:
    primary = page.evaluate("""() => {
        const host = document.querySelector(
            '.st-key-date_picker [data-testid="stBidiComponentRegular"]'
        );
        return host
            ? getComputedStyle(host).getPropertyValue('--st-primary-color').trim().toLowerCase()
            : '';
    }""")
    assert primary, "Streamlit did not expose --st-primary-color"
    assert primary != RSUITE_STOCK_PRIMARY, (
        "the fixture theme must differ from RSuite's stock primary or this "
        "suite cannot tell a working bridge from a missing one"
    )
    return primary


def test_rsuite_ramp_tracks_the_streamlit_primary(page: Page):
    """The 500 stop is the configured color exactly, not a shade near it."""
    primary = _configured_primary(page)

    ramp_500 = page.evaluate("""() => {
        const root = document.querySelector('.st-key-date_picker .react-root');
        return getComputedStyle(root)
            .getPropertyValue('--rs-primary-500')
            .trim()
            .toLowerCase();
    }""")

    assert ramp_500 == primary


def test_ramp_is_written_to_both_document_scopes(page: Page):
    """RSuite derives its semantic properties from the ramp with var(), and a
    var() resolves against the element its declaration sits on. The light theme
    declares those on :root and the dark theme redeclares them on body under
    .rs-theme-dark, so a ramp on only one of the two silently fails in the other
    appearance: on body alone, nothing in light mode changes color at all."""
    scopes = page.evaluate("""() => ({
        html: document.documentElement.style.getPropertyValue('--rs-primary-500').trim().toLowerCase(),
        body: document.body.style.getPropertyValue('--rs-primary-500').trim().toLowerCase(),
    })""")

    primary = _configured_primary(page)
    assert scopes["html"] == primary, "ramp missing from documentElement"
    assert scopes["body"] == primary, "ramp missing from body"


def test_selected_day_is_painted_in_the_app_primary(page: Page):
    """What a user actually sees. The calendar portals out to document.body, so
    this also covers the popup scope that a component-scoped ramp would miss."""
    primary = _configured_primary(page)

    page.locator(".st-key-date_picker input").first.click()
    selected = page.locator(
        ".rs-calendar-table-cell-selected .rs-calendar-table-cell-content"
    ).first
    expect(selected).to_be_visible()

    assert selected.evaluate(
        "el => getComputedStyle(el).backgroundColor"
    ) == _hex_to_rgb_string(primary)
