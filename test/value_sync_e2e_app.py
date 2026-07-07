"""Streamlit fixture app for the value-sync e2e test.

Drives the Python-side `value=` of two mounted components from Session State so
the test can change it at runtime and assert the widget adopts the new value
(the fix for the initial-only-hydration bug), while a user edit still
round-trips back to Python.
"""

import streamlit as st

from st_rsuite import check_tree, date_picker

st.title("st-rsuite value sync e2e")

TREE = [
    {
        "value": "frontend",
        "label": "Frontend",
        "children": [
            {"value": "react", "label": "React"},
            {"value": "vue", "label": "Vue"},
        ],
    }
]

st.session_state.setdefault("dp_value", "2026-06-22")
st.session_state.setdefault("ct_value", ["react"])

if st.button("set date", key="btn_date"):
    st.session_state.dp_value = "2030-01-01"
if st.button("set tree", key="btn_tree"):
    st.session_state.ct_value = ["vue"]

dp = date_picker(label="dp", value=st.session_state.dp_value, key="synced_dp")
st.html(f"<pre data-testid='echo-dp'>dp={dp}</pre>")

ct = check_tree(
    data=TREE,
    value=st.session_state.ct_value,
    cascade=False,  # 1:1 leaf checks, so the test can assert exact checked nodes
    default_expand_all=True,
    key="synced_ct",
)
st.html(f"<pre data-testid='echo-ct'>ct={sorted(ct)}</pre>")
