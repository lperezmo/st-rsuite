"""
st-rsuite Showcase
==================
Interactive demo of RSuite date & time components for Streamlit,
with side-by-side comparisons against standard widgets.
"""

import streamlit as st
from datetime import date, time, timedelta

from st_rsuite import (
    date_input,
    date_picker,
    date_range_input,
    date_range_picker,
    time_picker,
    time_range_picker,
)

# -- Page config -------------------------------------------------------------
st.set_page_config(
    page_title="st-rsuite | RSuite for Streamlit",
    page_icon=":material/calendar_month:",
    layout="wide",
)

st.markdown("""<style>
    .block-container {
        padding-top: 1rem;
    }
</style>""", unsafe_allow_html=True)

# -- Helpers: branded column banners -----------------------------------------
_IS_DARK = st.context.theme.type == "dark"

_RSUITE_BANNER_LIGHT = """
<div style="
    background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
    color: white;
    padding: 0.55rem 1rem;
    border-radius: 0.5rem;
    margin-bottom: 0.75rem;
    font-weight: 600;
    font-size: 0.85rem;
    display: flex; align-items: center; gap: 0.5rem;
    box-shadow: 0 2px 8px rgba(124,58,237,0.25);
">&#9670; st-rsuite</div>
"""

_RSUITE_BANNER_DARK = """
<div style="
    background: linear-gradient(135deg, #6d28d9 0%, #8b5cf6 100%);
    color: white;
    padding: 0.55rem 1rem;
    border-radius: 0.5rem;
    margin-bottom: 0.75rem;
    font-weight: 600;
    font-size: 0.85rem;
    display: flex; align-items: center; gap: 0.5rem;
    box-shadow: 0 2px 12px rgba(124,58,237,0.35);
">&#9670; st-rsuite</div>
"""

_ST_BANNER_LIGHT = """
<div style="
    background: linear-gradient(135deg, #64748b 0%, #94a3b8 100%);
    color: white;
    padding: 0.55rem 1rem;
    border-radius: 0.5rem;
    margin-bottom: 0.75rem;
    font-weight: 600;
    font-size: 0.85rem;
    display: flex; align-items: center; gap: 0.5rem;
    box-shadow: 0 2px 8px rgba(100,116,139,0.25);
">&#9671; Streamlit built-in</div>
"""

_ST_BANNER_DARK = """
<div style="
    background: linear-gradient(135deg, #475569 0%, #64748b 100%);
    color: #e2e8f0;
    padding: 0.55rem 1rem;
    border-radius: 0.5rem;
    margin-bottom: 0.75rem;
    font-weight: 600;
    font-size: 0.85rem;
    display: flex; align-items: center; gap: 0.5rem;
    box-shadow: 0 2px 12px rgba(71,85,105,0.35);
">&#9671; Streamlit built-in</div>
"""


def _banner_rsuite():
    st.html(_RSUITE_BANNER_DARK if _IS_DARK else _RSUITE_BANNER_LIGHT)


def _banner_st():
    st.html(_ST_BANNER_DARK if _IS_DARK else _ST_BANNER_LIGHT)


# -- Header ------------------------------------------------------------------
_HEADER_GRADIENT = (
    "linear-gradient(135deg, #a78bfa, #ddd6fe)"
    if _IS_DARK
    else "linear-gradient(135deg, #7c3aed, #6d28d9)"
)
st.html(f"""
<div style="text-align:center; padding:1.5rem 0 0.5rem;">
    <h1 style="
        margin:0; font-size:2.5rem; font-weight:800;
        background:{_HEADER_GRADIENT};
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
        background-clip:text;
    ">st-rsuite</h1>
    <p style="margin:0.4rem 0 0; font-size:1rem; opacity:0.7;">
        RSuite date &amp; time components for Streamlit, powered by Components v2
    </p>
</div>
""")

# -- Sidebar: global controls ------------------------------------------------
with st.sidebar:
    st.header("Global Settings")
    disabled = st.toggle("Disable all components", value=False)
    st.divider()
    st.markdown(
        "**st-rsuite** brings RSuite's production-grade date & time components "
        "to Streamlit using the new Components v2 API. All components are MIT licensed."
    )
    st.markdown("**Pickers** — rich popups:")
    st.markdown("- :material/event: DatePicker")
    st.markdown("- :material/date_range: DateRangePicker")
    st.markdown("- :material/schedule: TimePicker")
    st.markdown("- :material/schedule: TimeRangePicker")
    st.markdown("**Inputs** — simple keyboard-only:")
    st.markdown("- :material/keyboard: DateInput")
    st.markdown("- :material/keyboard: DateRangeInput")

# -- Component selector ------------------------------------------------------
selected = st.segmented_control(
    "Component",
    options=[
        ":material/event: DatePicker",
        ":material/date_range: DateRangePicker",
        ":material/schedule: TimePicker",
        ":material/schedule: TimeRangePicker",
        ":material/keyboard: DateInput",
        ":material/keyboard: DateRangeInput",
    ],
    default=":material/event: DatePicker",
)

# ============================================================================
# DATE PICKER
# ============================================================================
if selected == ":material/event: DatePicker":
    st.subheader("DatePicker")
    st.markdown(
        "A date picker with calendar popup, one-tap mode, "
        "ISO week support, and customizable format."
    )

    st.markdown("#### Basic")

    with st.container(horizontal=True):
        _banner_rsuite()
        dp = date_picker(
            label="Pick any date",
            value=date.today(),
            one_tap=True,
            disabled=disabled,
            key="dp_basic",
        )
        st.code(f"Selected: {dp}")

    with st.container(horizontal=True):
        _banner_st()
        dp_st = st.date_input(
            "Pick any date",
            value=date.today(),
            disabled=disabled,
            key="st_dp_basic",
        )
        st.code(f"Selected: {dp_st}")

    st.divider()

    st.markdown("#### One-tap mode")

    with st.container(horizontal=True):
        _banner_rsuite()
        dp2 = date_picker(
            label="One-click select",
            one_tap=True,
            disabled=disabled,
            key="dp_onetap",
        )
        st.code(f"Selected: {dp2}")

    st.divider()

    st.markdown("#### ISO week + week numbers")

    with st.container(horizontal=True):
        _banner_rsuite()
        dp3 = date_picker(
            label="ISO week picker",
            iso_week=True,
            show_week_numbers=True,
            disabled=disabled,
            key="dp_iso",
        )
        st.code(f"Selected: {dp3}")

    with st.expander("Usage code"):
        st.code(
            '''from st_rsuite import date_picker
from datetime import date

selected = date_picker(
    label="Pick a date",
    value=date.today(),
    format="yyyy-MM-dd",
    one_tap=True,
    key="my_date",
)''',
            language="python",
        )

# ============================================================================
# DATE RANGE PICKER
# ============================================================================
elif selected == ":material/date_range: DateRangePicker":
    st.subheader("DateRangePicker")
    st.markdown(
        "Full-featured dual-calendar popup for selecting date ranges. "
        "Supports hover highlighting, one-tap mode, and single-calendar mode."
    )

    st.markdown("#### Basic")

    with st.container(horizontal=True):
        _banner_rsuite()
        drp = date_range_picker(
            label="Trip dates",
            value=(date.today(), date.today() + timedelta(days=7)),
            disabled=disabled,
            key="drp_basic",
        )
        st.code(f"Start: {drp[0]}  End: {drp[1]}")

    with st.container(horizontal=True):
        _banner_st()
        drp_st = st.date_input(
            "Trip dates",
            value=(date.today(), date.today() + timedelta(days=7)),
            disabled=disabled,
            key="st_drp_basic",
        )
        if isinstance(drp_st, tuple) and len(drp_st) == 2:
            st.code(f"Start: {drp_st[0]}  End: {drp_st[1]}")
        else:
            st.code(f"Selected: {drp_st}")

    st.divider()

    st.markdown("#### Single calendar + one-tap")

    with st.container(horizontal=True):
        _banner_rsuite()
        drp2 = date_range_picker(
            label="Quick range",
            show_one_calendar=True,
            one_tap=True,
            disabled=disabled,
            key="drp_single",
        )
        st.code(f"Start: {drp2[0]}  End: {drp2[1]}")

    st.divider()

    st.markdown("#### Hover range: week")

    with st.container(horizontal=True):
        _banner_rsuite()
        drp3 = date_range_picker(
            label="Select a week",
            hover_range="week",
            one_tap=True,
            disabled=disabled,
            key="drp_hover",
        )
        st.code(f"Start: {drp3[0]}  End: {drp3[1]}")

    with st.expander("Usage code"):
        st.code(
            '''from st_rsuite import date_range_picker
from datetime import date, timedelta

start, end = date_range_picker(
    label="Trip dates",
    value=(date.today(), date.today() + timedelta(days=7)),
    hover_range="week",
    one_tap=True,
    key="my_range",
)''',
            language="python",
        )

# ============================================================================
# TIME PICKER
# ============================================================================
elif selected == ":material/schedule: TimePicker":
    st.subheader("TimePicker")
    st.markdown(
        "A time picker with scrolling time panel and optional AM/PM."
    )
    st.caption(
        "Note: On Streamlit Community Cloud, the \"Hosted with Streamlit\" badge "
        "may cover the OK button on time pickers. This is not an issue on "
        "self-hosted or locally-hosted apps."
    )

    st.markdown("#### 24-hour format")

    with st.container(horizontal=True):
        _banner_rsuite()
        tp = time_picker(
            label="Pick a time",
            value=time(14, 30),
            disabled=disabled,
            key="tp_24h",
        )
        st.code(f"Selected: {tp}")

    with st.container(horizontal=True):
        _banner_st()
        tp_st = st.time_input(
            "Pick a time",
            value=time(14, 30),
            disabled=disabled,
            key="st_tp_24h",
        )
        st.code(f"Selected: {tp_st}")

    st.divider()

    st.markdown("#### 12-hour (AM/PM)")

    with st.container(horizontal=True):
        _banner_rsuite()
        tp2 = time_picker(
            label="Pick a time (12h)",
            value=time(9, 30),
            format="hh:mm aa",
            show_meridiem=True,
            disabled=disabled,
            key="tp_12h",
        )
        st.code(f"Selected: {tp2}")

    with st.expander("Usage code"):
        st.code(
            '''from st_rsuite import time_picker
from datetime import time

selected = time_picker(
    label="Pick a time",
    value=time(9, 30),
    format="hh:mm aa",
    show_meridiem=True,
    key="my_time",
)''',
            language="python",
        )

# ============================================================================
# TIME RANGE PICKER
# ============================================================================
elif selected == ":material/schedule: TimeRangePicker":
    st.subheader("TimeRangePicker")
    st.markdown(
        "Select a time range with start and end time panels."
    )
    st.caption(
        "Note: On Streamlit Community Cloud, the \"Hosted with Streamlit\" badge "
        "may cover the OK button on time pickers. This is not an issue on "
        "self-hosted or locally-hosted apps."
    )

    st.markdown("#### Basic")

    with st.container(horizontal=True):
        _banner_rsuite()
        trp = time_range_picker(
            label="Shift hours",
            value=(time(9, 0), time(17, 0)),
            disabled=disabled,
            key="trp_basic",
        )
        st.code(f"Start: {trp[0]}  End: {trp[1]}")

    st.divider()

    st.markdown("#### 12-hour with AM/PM")

    with st.container(horizontal=True):
        _banner_rsuite()
        trp2 = time_range_picker(
            label="Meeting time",
            value=(time(10, 0), time(11, 30)),
            format="hh:mm aa",
            show_meridiem=True,
            character=" to ",
            disabled=disabled,
            key="trp_12h",
        )
        st.code(f"Start: {trp2[0]}  End: {trp2[1]}")

    with st.expander("Usage code"):
        st.code(
            '''from st_rsuite import time_range_picker
from datetime import time

start, end = time_range_picker(
    label="Shift hours",
    value=(time(9, 0), time(17, 0)),
    format="hh:mm aa",
    show_meridiem=True,
    key="my_time_range",
)''',
            language="python",
        )

# ============================================================================
# DATE INPUT (simple, keyboard-only)
# ============================================================================
elif selected == ":material/keyboard: DateInput":
    st.subheader("DateInput")
    st.caption("Simple keyboard-only — no popup, meant for compact quick-entry scenarios.")

    st.markdown("#### Basic")

    with st.container(horizontal=True):
        _banner_rsuite()
        di = date_input(
            label="Enter a date",
            value=date.today(),
            disabled=disabled,
            key="di_basic",
        )
        st.code(f"Selected: {di}")

    with st.container(horizontal=True):
        _banner_st()
        di_st = st.date_input(
            "Enter a date",
            value=date.today(),
            disabled=disabled,
            key="st_di_basic",
        )
        st.code(f"Selected: {di_st}")

    st.divider()

    st.markdown("#### Custom format")

    with st.container(horizontal=True):
        _banner_rsuite()
        di2 = date_input(
            label="MM/dd/yyyy format",
            value=date(2026, 3, 14),
            format="MM/dd/yyyy",
            disabled=disabled,
            key="di_format",
        )
        st.code(f"Selected: {di2}")

    with st.expander("Usage code"):
        st.code(
            '''from st_rsuite import date_input
from datetime import date

selected = date_input(
    label="Enter a date",
    value=date.today(),
    format="yyyy-MM-dd",
    key="my_date_input",
)''',
            language="python",
        )

# ============================================================================
# DATE RANGE INPUT (simple, keyboard-only)
# ============================================================================
elif selected == ":material/keyboard: DateRangeInput":
    st.subheader("DateRangeInput")
    st.caption("Simple keyboard-only — no popup, designed for straightforward date range entry.")

    st.markdown("#### Basic")

    with st.container(horizontal=True):
        _banner_rsuite()
        dri = date_range_input(
            label="Enter date range",
            value=(date.today(), date.today() + timedelta(days=7)),
            disabled=disabled,
            key="dri_basic",
        )
        st.code(f"Start: {dri[0]}  End: {dri[1]}")

    with st.container(horizontal=True):
        _banner_st()
        dri_st = st.date_input(
            "Enter date range",
            value=(date.today(), date.today() + timedelta(days=7)),
            disabled=disabled,
            key="st_dri_basic",
        )
        if isinstance(dri_st, tuple) and len(dri_st) == 2:
            st.code(f"Start: {dri_st[0]}  End: {dri_st[1]}")
        else:
            st.code(f"Selected: {dri_st}")

    st.divider()

    st.markdown("#### Custom separator")

    with st.container(horizontal=True):
        _banner_rsuite()
        dri2 = date_range_input(
            label="Custom separator",
            value=(date(2026, 3, 1), date(2026, 3, 15)),
            character=" to ",
            disabled=disabled,
            key="dri_sep",
        )
        st.code(f"Start: {dri2[0]}  End: {dri2[1]}")

    with st.expander("Usage code"):
        st.code(
            '''from st_rsuite import date_range_input
from datetime import date, timedelta

start, end = date_range_input(
    label="Enter date range",
    value=(date.today(), date.today() + timedelta(days=7)),
    character=" to ",
    key="my_range_input",
)''',
            language="python",
        )

# -- Footer ------------------------------------------------------------------
st.divider()
st.caption(
    "Built with [st-rsuite](https://github.com/lperezmo/st-rsuite) · "
    "Based on [RSuite](https://rsuitejs.com/) · "
    "Streamlit Components v2"
)
