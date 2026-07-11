"""Streamlit fixture app for the cascader / tree_picker e2e tests."""

import streamlit as st

from st_rsuite import cascader, tree_picker

CASCADE = [
    {
        "value": "us",
        "label": "United States",
        "children": [
            {
                "value": "ca",
                "label": "California",
                "children": [
                    {"value": "sf", "label": "San Francisco"},
                    {"value": "la", "label": "Los Angeles"},
                ],
            }
        ],
    },
    {
        "value": "uk",
        "label": "United Kingdom",
        "children": [{"value": "lon", "label": "London"}],
    },
]

TREE = [
    {
        "value": "frontend",
        "label": "Frontend",
        "children": [
            {"value": "react", "label": "React"},
            {"value": "vue", "label": "Vue"},
        ],
    },
    {
        "value": "backend",
        "label": "Backend",
        "children": [{"value": "python", "label": "Python"}],
    },
]

cas = cascader(data=CASCADE, label="City", key="cas")
st.html(f"<pre data-testid='echo-cas'>cas={cas}</pre>")

tpv = tree_picker(
    data=TREE,
    label="Tech",
    default_expand_all=True,
    only_leaf_selectable=True,
    key="tpv",
)
st.html(f"<pre data-testid='echo-tpv'>tpv={tpv}</pre>")
