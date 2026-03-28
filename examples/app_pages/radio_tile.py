import streamlit as st

from st_rsuite import radio_tile
from utils.ui import banner_rsuite

disabled = st.session_state.get("disabled", False)

st.markdown(
    "A tile-based radio group for visually rich single-selection. "
    "Each tile can have an icon, label, and description."
)

st.markdown("#### Basic")

banner_rsuite()
rt = radio_tile(
    options=[
        {"value": "react", "label": "React", "description": "A JavaScript library for building user interfaces", "icon": "R"},
        {"value": "vue", "label": "Vue", "description": "The progressive JavaScript framework", "icon": "V"},
        {"value": "angular", "label": "Angular", "description": "Platform for building mobile and desktop web apps", "icon": "A"},
    ],
    value="react",
    disabled=disabled,
    key="rt_basic",
)
st.code(f"Selected: {rt}")

st.divider()

st.markdown("#### Inline layout")

banner_rsuite()
rt2 = radio_tile(
    options=[
        {"value": "s", "label": "Small", "description": "1 vCPU, 1 GB RAM"},
        {"value": "m", "label": "Medium", "description": "2 vCPU, 4 GB RAM"},
        {"value": "l", "label": "Large", "description": "4 vCPU, 16 GB RAM"},
        {"value": "xl", "label": "XL", "description": "8 vCPU, 32 GB RAM"},
    ],
    value="m",
    inline=True,
    disabled=disabled,
    key="rt_inline",
)
st.code(f"Selected: {rt2}")

st.divider()

st.markdown("#### With emoji icons")

banner_rsuite()
rt3 = radio_tile(
    options=[
        {"value": "light", "label": "Light", "description": "Classic light theme", "icon": "\u2600\uFE0F"},
        {"value": "dark", "label": "Dark", "description": "Easy on the eyes", "icon": "\U0001F319"},
        {"value": "auto", "label": "Auto", "description": "Follow system preference", "icon": "\u2699\uFE0F"},
    ],
    value="auto",
    inline=True,
    disabled=disabled,
    key="rt_icons",
)
st.code(f"Selected: {rt3}")

with st.expander("Usage code", icon=":material/code:"):
    st.code(
        '''from st_rsuite import radio_tile

selected = radio_tile(
    options=[
        {"value": "a", "label": "Option A", "description": "Desc A", "icon": "\u2600\ufe0f"},
        {"value": "b", "label": "Option B", "description": "Desc B", "icon": "\u2699\ufe0f"},
    ],
    value="a",
    inline=True,
    key="my_radio_tile",
)''',
        language="python",
    )
