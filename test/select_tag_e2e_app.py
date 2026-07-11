"""Streamlit fixture app for the select_picker / tag_picker e2e tests."""

import streamlit as st

from st_rsuite import select_picker, tag_picker

ITEMS = [
    {"value": "react", "label": "React", "group": "Frontend"},
    {"value": "vue", "label": "Vue", "group": "Frontend"},
    {"value": "django", "label": "Django", "group": "Backend"},
    {"value": "fastapi", "label": "FastAPI", "group": "Backend"},
]

sp = select_picker(
    items=ITEMS,
    value="react",
    label="Framework",
    disabled_items=["django"],
    key="sp",
)
st.html(f"<pre data-testid='echo-sp'>sp={sp}</pre>")

tp = tag_picker(
    items=ITEMS,
    value=["react"],
    label="Stack",
    creatable=True,
    key="tp",
)
st.html(f"<pre data-testid='echo-tp'>tp={'|'.join(tp)}</pre>")
