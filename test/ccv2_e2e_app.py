"""Streamlit fixture app for the CCv2 e2e tests.

Renders all 13 st-rsuite components with stable defaults and echoes each return
value through a `data-testid` element so the tests can assert the Python <-> JS
round-trip. Every component uses `key=<name>`, so tests target
`.st-key-<name> .stBidiComponent`.
"""

from datetime import date, time

import streamlit as st

from st_rsuite import (
    carousel,
    check_tree,
    check_tree_picker,
    date_input,
    date_picker,
    date_range_input,
    date_range_picker,
    multi_cascade_tree,
    pin_input,
    radio_tile,
    time_picker,
    time_range_picker,
    timeline,
)

st.title("st-rsuite CCv2 e2e")

D1 = date(2026, 6, 22)
D2 = date(2026, 6, 29)


def echo(testid: str, value: str) -> None:
    st.html(f"<pre data-testid='{testid}'>{value}</pre>")


# -- Pickers -----------------------------------------------------------------
dp = date_picker(label="date_picker", value=D1, key="date_picker")
echo("echo-date_picker", f"dp={dp}")

drp = date_range_picker(label="date_range_picker", value=(D1, D2), key="date_range_picker")
echo("echo-date_range_picker", f"drp={drp[0]}|{drp[1]}")

tp = time_picker(label="time_picker", value=time(9, 30), key="time_picker")
echo("echo-time_picker", f"tp={tp}")

trp = time_range_picker(
    label="time_range_picker", value=(time(9, 0), time(17, 0)), key="time_range_picker"
)
echo("echo-time_range_picker", f"trp={trp[0]}|{trp[1]}")

# -- Inputs ------------------------------------------------------------------
di = date_input(label="date_input", value=D1, key="date_input")
echo("echo-date_input", f"di={di}")

dri = date_range_input(label="date_range_input", value=(D1, D2), key="date_range_input")
echo("echo-date_range_input", f"dri={dri[0]}|{dri[1]}")

# -- Selection ---------------------------------------------------------------
rt = radio_tile(
    options=[
        {"value": "a", "label": "Option A", "description": "first"},
        {"value": "b", "label": "Option B", "description": "second"},
    ],
    value="a",
    inline=True,
    key="radio_tile",
)
echo("echo-radio_tile", f"rt={rt}")

# -- Trees -------------------------------------------------------------------
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

ctv = check_tree(data=TREE, value=["react"], key="check_tree")
echo("echo-check_tree", f"ct={sorted(ctv)}")

ctpv = check_tree_picker(data=TREE, value=["react"], key="check_tree_picker")
echo("echo-check_tree_picker", f"ctp={sorted(ctpv)}")

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
mctv = multi_cascade_tree(data=CASCADE, value=["sf"], key="multi_cascade_tree")
echo("echo-multi_cascade_tree", f"mct={sorted(mctv)}")

# -- Display & input ---------------------------------------------------------
car = carousel(
    items=[
        {"content": "Slide 1", "background": "#7c3aed"},
        {"content": "Slide 2", "background": "#6d28d9"},
    ],
    autoplay=False,
    key="carousel",
)
echo("echo-carousel", f"car={car}")

timeline(
    items=[
        {"content": "Order placed", "time": "10:00"},
        {"content": "Shipped", "time": "14:30"},
    ],
    key="timeline",
)

pin = pin_input(length=6, value="123456", key="pin_input")
echo("echo-pin_input", f"pin={pin}")
