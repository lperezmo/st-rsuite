"""Streamlit fixture app for the review-findings e2e regression tests.

Renders exactly the configurations the reviewed defects needed:

- ``date_input`` / ``date_range_input`` handed ``datetime`` (not ``date``)
  defaults, which used to serialize to a full timestamp and render empty,
- a disabled ``check_tree`` and ``multi_cascade_tree``, which must be
  keyboard-proof and not only mouse-proof,
- a ``tag_picker`` whose Python-driven value flips between ``["New York"]`` and
  ``["New", "York"]``, two lists that only stay distinct while the sync key
  joins on NUL,
- a ``date_picker`` that can be forced to re-render so the theme bridge has to
  re-detect Streamlit's appearance instead of serving a stale cache.
"""

from datetime import date, datetime

import streamlit as st

from st_rsuite import (
    check_tree,
    date_input,
    date_picker,
    date_range_input,
    multi_cascade_tree,
    tag_picker,
)

st.title("st-rsuite review findings e2e")


def echo(testid: str, value: str) -> None:
    st.html(f"<pre data-testid='{testid}'>{value}</pre>")


# -- datetime defaults -------------------------------------------------------
DT_START = datetime(2026, 6, 22, 3, 4, 5)
DT_END = datetime(2026, 6, 29, 23, 59, 59)

di = date_input(value=DT_START, key="dt_di")
echo("echo-dt_di", f"di={di}")

dri = date_range_input(value=(DT_START, DT_END), key="dt_dri")
echo("echo-dt_dri", f"dri={dri[0]}|{dri[1]}")

# -- disabled trees ----------------------------------------------------------
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

ct = check_tree(
    data=TREE,
    value=["react"],
    cascade=False,
    default_expand_all=True,
    disabled=True,
    key="disabled_ct",
)
echo("echo-disabled_ct", f"ct={sorted(ct)}")

CASCADE = [
    {
        "value": "us",
        "label": "US",
        "children": [
            {
                "value": "ca",
                "label": "California",
                "children": [{"value": "sf", "label": "San Francisco"}],
            }
        ],
    }
]

mct = multi_cascade_tree(
    data=CASCADE, value=["sf"], cascade=False, disabled=True, key="disabled_mct"
)
echo("echo-disabled_mct", f"mct={sorted(mct)}")

# -- tag picker sync-key collision -------------------------------------------
CITY_ITEMS = [
    {"value": "New York", "label": "New York"},
    {"value": "New", "label": "New"},
    {"value": "York", "label": "York"},
]

if st.button("split tags"):
    st.session_state["tags_from_python"] = ["New", "York"]

tp = tag_picker(
    items=CITY_ITEMS,
    value=st.session_state.get("tags_from_python", ["New York"]),
    key="collide_tp",
)
echo("echo-collide_tp", f"tp={'|'.join(tp)}")

# -- theme re-detection ------------------------------------------------------
# The button changes this picker's data, so Streamlit re-renders it and the
# theme bridge has to resolve the appearance again.
if st.button("rerender"):
    st.session_state["renders"] = st.session_state.get("renders", 0) + 1

date_picker(
    label=f"render {st.session_state.get('renders', 0)}",
    value=date(2026, 6, 22),
    key="themed_dp",
)

st.html("<pre data-testid='ready'>ready</pre>")
