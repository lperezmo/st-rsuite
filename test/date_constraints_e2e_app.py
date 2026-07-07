"""Streamlit fixture app for the date-constraints e2e test.

Renders a date_picker constrained to a single week of June 2026 so the test can
open the calendar and assert that dates outside the range, plus explicitly
disabled dates and disabled weekdays, are non-selectable.
"""

from datetime import date

import streamlit as st

from st_rsuite import date_picker

st.title("st-rsuite date constraints e2e")

dp = date_picker(
    label="constrained",
    value=date(2026, 6, 22),
    min_date=date(2026, 6, 15),
    max_date=date(2026, 6, 26),
    disabled_dates=[date(2026, 6, 24)],
    disabled_weekdays=[5, 6],  # Saturday and Sunday
    key="constrained_dp",
)
st.html(f"<pre data-testid='echo-dp'>dp={dp}</pre>")
