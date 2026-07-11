"""Streamlit fixture app for the single-bundle e2e test.

Renders several widget kinds on one page (one localized to ja_JP so the lazy
locale chunk is exercised) and echoes the last value so the test knows the
first script run finished. Every widget uses `key=<name>`, so the test targets
`.st-key-<name> .stBidiComponent`.
"""

from datetime import date, time

import streamlit as st

from st_rsuite import check_tree, date_picker, pin_input, time_picker

st.title("st-rsuite single-bundle e2e")

D1 = date(2026, 6, 22)

date_picker(label="date_picker", value=D1, key="date_picker")
time_picker(label="time_picker", value=time(9, 30), key="time_picker")
check_tree(
    data=[
        {
            "value": "frontend",
            "label": "Frontend",
            "children": [{"value": "react", "label": "React"}],
        }
    ],
    value=["react"],
    key="check_tree",
)
date_picker(label="date_picker_ja", value=D1, locale="ja_JP", key="date_picker_ja")

pin = pin_input(length=6, value="123456", key="pin_input")
st.html(f"<pre data-testid='echo-pin_input'>pin={pin}</pre>")
