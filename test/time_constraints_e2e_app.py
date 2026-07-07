"""Streamlit fixture app for the time-constraints e2e test.

A time_picker restricted to business hours (09:00-17:00) so the test can open
the panel and assert out-of-window hours are absent from the hour column.
"""

from datetime import time

import streamlit as st

from st_rsuite import time_picker

st.title("st-rsuite time constraints e2e")

tp = time_picker(
    label="business hours",
    value=time(9, 0),
    min_hour=9,
    max_hour=17,
    key="business_tp",
)
st.html(f"<pre data-testid='echo-tp'>tp={tp}</pre>")
