"""Streamlit fixture app for the accessibility e2e test.

Renders the six labeled date/time components (each with a label and help text)
so the test can assert every label is associated to a control id and the help
tooltip is present.
"""

from datetime import date, time

import streamlit as st

from st_rsuite import (
    date_input,
    date_picker,
    date_range_input,
    date_range_picker,
    time_picker,
    time_range_picker,
)

st.title("st-rsuite a11y e2e")

date_picker(label="date_picker", value=date(2026, 6, 22), help="dp help", key="dp")
date_range_picker(
    label="date_range_picker",
    value=(date(2026, 6, 1), date(2026, 6, 7)),
    help="drp help",
    key="drp",
)
time_picker(label="time_picker", value=time(9, 30), help="tp help", key="tp")
time_range_picker(
    label="time_range_picker",
    value=(time(9, 0), time(17, 0)),
    help="trp help",
    key="trp",
)
date_input(label="date_input", value=date(2026, 6, 22), help="di help", key="di")
date_range_input(
    label="date_range_input",
    value=(date(2026, 6, 1), date(2026, 6, 7)),
    help="dri help",
    key="dri",
)
st.html("<pre data-testid='ready'>ready</pre>")
