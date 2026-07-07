"""Streamlit fixture app for the range-shortcuts e2e test.

A date_range_picker with two custom shortcut presets so the test can open the
overlay, click a preset, and assert it selects the expected range.
"""

from datetime import date

import streamlit as st

from st_rsuite import date_range_picker

st.title("st-rsuite range shortcuts e2e")

drp = date_range_picker(
    label="report window",
    ranges=[
        {"label": "June week", "value": (date(2026, 6, 15), date(2026, 6, 21))},
        {"label": "Single day", "value": (date(2026, 6, 10), date(2026, 6, 10))},
    ],
    key="preset_drp",
)
st.html(f"<pre data-testid='echo-drp'>drp={drp[0]}|{drp[1]}</pre>")
