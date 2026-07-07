import streamlit as st
from datetime import date, timedelta

from st_rsuite import date_picker, date_range_picker
from utils.ui import banner_rsuite, banner_st

disabled = st.session_state.get("disabled", False)

st.markdown(
    "Date pickers with calendar popups, one-tap mode, "
    "ISO week support, and customizable format."
)

# -- DatePicker --------------------------------------------------------------
st.subheader("DatePicker")

st.markdown("#### Basic")

with st.container(horizontal=True):
    banner_rsuite()
    dp = date_picker(
        label="Pick any date",
        value=date.today(),
        one_tap=True,
        disabled=disabled,
        key="dp_basic",
    )
    st.code(f"Selected: {dp}")

with st.container(horizontal=True):
    banner_st()
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
    banner_rsuite()
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
    banner_rsuite()
    dp3 = date_picker(
        label="ISO week picker",
        iso_week=True,
        show_week_numbers=True,
        disabled=disabled,
        key="dp_iso",
    )
    st.code(f"Selected: {dp3}")

st.divider()

st.markdown("#### Constraints (min/max, disabled weekdays)")

_today = date.today()
with st.container(horizontal=True):
    banner_rsuite()
    dp4 = date_picker(
        label="Weekdays only, next 30 days",
        value=_today,
        min_date=_today,
        max_date=_today + timedelta(days=30),
        disabled_weekdays=[5, 6],  # 0=Monday .. 6=Sunday, so Sat/Sun
        one_tap=True,
        disabled=disabled,
        key="dp_constrained",
    )
    st.code(f"Selected: {dp4}")

with st.expander("Usage code", icon=":material/code:"):
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

# -- DateRangePicker ---------------------------------------------------------
st.divider()
st.subheader("DateRangePicker")
st.markdown(
    "Full-featured dual-calendar popup for selecting date ranges. "
    "Supports hover highlighting, one-tap mode, and single-calendar mode."
)

st.markdown("#### Basic")

with st.container(horizontal=True):
    banner_rsuite()
    drp = date_range_picker(
        label="Trip dates",
        value=(date.today(), date.today() + timedelta(days=7)),
        disabled=disabled,
        key="drp_basic",
    )
    st.code(f"Start: {drp[0]}  End: {drp[1]}")

with st.container(horizontal=True):
    banner_st()
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
    banner_rsuite()
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
    banner_rsuite()
    drp3 = date_range_picker(
        label="Select a week",
        hover_range="week",
        one_tap=True,
        disabled=disabled,
        key="drp_hover",
    )
    st.code(f"Start: {drp3[0]}  End: {drp3[1]}")

st.divider()

st.markdown("#### Shortcut ranges")

_today = date.today()
with st.container(horizontal=True):
    banner_rsuite()
    drp4 = date_range_picker(
        label="Report window",
        ranges=[
            {"label": "Last 7 days", "value": (_today - timedelta(days=6), _today)},
            {"label": "Last 30 days", "value": (_today - timedelta(days=29), _today)},
            {"label": "This month", "value": (_today.replace(day=1), _today)},
        ],
        key="drp_ranges",
    )
    st.code(f"Start: {drp4[0]}  End: {drp4[1]}")

with st.expander("Usage code", icon=":material/code:"):
    st.code(
        '''from st_rsuite import date_range_picker
from datetime import date, timedelta

today = date.today()
start, end = date_range_picker(
    label="Report window",
    hover_range="week",
    ranges=[
        {"label": "Last 7 days", "value": (today - timedelta(days=6), today)},
        {"label": "This month", "value": (today.replace(day=1), today)},
    ],
    key="my_range",
)''',
        language="python",
    )
