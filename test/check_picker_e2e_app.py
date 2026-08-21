"""Streamlit fixture app for the check_picker e2e tests."""

import streamlit as st

from st_rsuite import check_picker, tag_picker

ITEMS = [
    {"value": "react", "label": "React", "group": "Frontend"},
    {"value": "vue", "label": "Vue", "group": "Frontend"},
    {"value": "django", "label": "Django", "group": "Backend"},
    {"value": "fastapi", "label": "FastAPI", "group": "Backend"},
]

ckp = check_picker(
    items=ITEMS,
    value=["react"],
    label="Framework",
    disabled_items=["django"],
    key="ckp",
)
st.html(f"<pre data-testid='echo-ckp'>ckp={'|'.join(ckp)}</pre>")

ckp_subtle = check_picker(
    items=ITEMS,
    appearance="subtle",
    placeholder="Subtle",
    key="ckp_subtle",
)
st.html(
    "<pre data-testid='echo-ckp-subtle'>ckp_subtle="
    f"{'|'.join(ckp_subtle)}</pre>"
)

tp = tag_picker(items=ITEMS, appearance="subtle", key="tp")
st.html(f"<pre data-testid='echo-tp'>tp={'|'.join(tp)}</pre>")
