"""Streamlit fixture app for the popup anchoring e2e test.

Renders pickers on a page tall enough to scroll so the test can open a popup,
scroll Streamlit's main section, and assert that the popup follows its toggle,
flips above it near the bottom edge, and hides once the toggle scrolls away.
"""

from datetime import date

import streamlit as st

from st_rsuite import date_picker, select_picker

st.title("st-rsuite popup anchoring e2e")

# A picker near the top of the page: scrolling down moves it toward the top
# edge and then out of view.
dp = date_picker(label="anchored", value=date(2026, 6, 22), key="anchored_dp")
st.html(f"<pre data-testid='echo-dp'>dp={dp}</pre>")

# Filler so the main section scrolls and the lower picker starts below the
# fold, where opening it downward would not fit.
for i in range(40):
    st.text(f"filler line {i}")

sp = select_picker(
    label="lower",
    items=[{"label": f"option {i}", "value": f"o{i}"} for i in range(6)],
    key="lower_sp",
)
st.html(f"<pre data-testid='echo-sp'>sp={sp}</pre>")

for i in range(40, 80):
    st.text(f"filler line {i}")
