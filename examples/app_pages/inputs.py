import streamlit as st
from datetime import date, timedelta

from st_rsuite import date_input, date_range_input
from utils.ui import banner_rsuite, banner_st

disabled = st.session_state.get("disabled", False)

st.markdown("Simple keyboard-only date entry — no popup, meant for compact quick-entry scenarios.")

# -- DateInput ---------------------------------------------------------------
st.subheader("DateInput")

st.markdown("#### Basic")

with st.container(horizontal=True):
    banner_rsuite()
    di = date_input(
        label="Enter a date",
        value=date.today(),
        disabled=disabled,
        key="di_basic",
    )
    st.code(f"Selected: {di}")

with st.container(horizontal=True):
    banner_st()
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
    banner_rsuite()
    di2 = date_input(
        label="MM/dd/yyyy format",
        value=date(2026, 3, 14),
        format="MM/dd/yyyy",
        disabled=disabled,
        key="di_format",
    )
    st.code(f"Selected: {di2}")

with st.expander("Usage code", icon=":material/code:"):
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

# -- DateRangeInput ----------------------------------------------------------
st.divider()
st.subheader("DateRangeInput")

st.markdown("#### Basic")

with st.container(horizontal=True):
    banner_rsuite()
    dri = date_range_input(
        label="Enter date range",
        value=(date.today(), date.today() + timedelta(days=7)),
        disabled=disabled,
        key="dri_basic",
    )
    st.code(f"Start: {dri[0]}  End: {dri[1]}")

with st.container(horizontal=True):
    banner_st()
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
    banner_rsuite()
    dri2 = date_range_input(
        label="Custom separator",
        value=(date(2026, 3, 1), date(2026, 3, 15)),
        character=" to ",
        disabled=disabled,
        key="dri_sep",
    )
    st.code(f"Start: {dri2[0]}  End: {dri2[1]}")

with st.expander("Usage code", icon=":material/code:"):
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
