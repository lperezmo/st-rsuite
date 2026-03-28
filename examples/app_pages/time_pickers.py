import streamlit as st
from datetime import time

from st_rsuite import time_picker, time_range_picker
from utils.ui import banner_rsuite, banner_st

disabled = st.session_state.get("disabled", False)

st.caption(
    "Note: On Streamlit Community Cloud, the \"Hosted with Streamlit\" badge "
    "may cover the OK button on time pickers. This is not an issue on "
    "self-hosted or locally-hosted apps."
)

# -- TimePicker --------------------------------------------------------------
st.subheader("TimePicker")
st.markdown("A time picker with scrolling time panel and optional AM/PM.")

st.markdown("#### 24-hour format")

with st.container(horizontal=True):
    banner_rsuite()
    tp = time_picker(
        label="Pick a time",
        value=time(14, 30),
        disabled=disabled,
        key="tp_24h",
    )
    st.code(f"Selected: {tp}")

with st.container(horizontal=True):
    banner_st()
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
    banner_rsuite()
    tp2 = time_picker(
        label="Pick a time (12h)",
        value=time(9, 30),
        format="hh:mm aa",
        show_meridiem=True,
        disabled=disabled,
        key="tp_12h",
    )
    st.code(f"Selected: {tp2}")

with st.expander("Usage code", icon=":material/code:"):
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

# -- TimeRangePicker ---------------------------------------------------------
st.divider()
st.subheader("TimeRangePicker")
st.markdown("Select a time range with start and end time panels.")

st.markdown("#### Basic")

with st.container(horizontal=True):
    banner_rsuite()
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
    banner_rsuite()
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

with st.expander("Usage code", icon=":material/code:"):
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
