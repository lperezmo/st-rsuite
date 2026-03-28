"""
st-rsuite Showcase
==================
Interactive demo of all 13 RSuite components for Streamlit,
with side-by-side comparisons against standard widgets.
"""

import streamlit as st

# -- Page config (must be first Streamlit call) ------------------------------
st.set_page_config(
    page_title="st-rsuite | RSuite for Streamlit",
    page_icon=":material/calendar_month:",
    layout="wide",
)

st.markdown("""<style>
    .block-container {
        padding-top: 1rem;
    }
</style>""", unsafe_allow_html=True)

# -- Global state (runs before every page) -----------------------------------
st.session_state.setdefault("disabled", False)

# -- Navigation --------------------------------------------------------------
page = st.navigation(
    {
        "": [
            st.Page("app_pages/date_pickers.py", title="Date pickers", icon=":material/event:"),
            st.Page("app_pages/time_pickers.py", title="Time pickers", icon=":material/schedule:"),
            st.Page("app_pages/inputs.py", title="Date inputs", icon=":material/keyboard:"),
        ],
        "Selection": [
            st.Page("app_pages/radio_tile.py", title="RadioTile", icon=":material/grid_view:"),
        ],
        "Trees": [
            st.Page("app_pages/trees.py", title="Tree components", icon=":material/account_tree:"),
        ],
        "Display": [
            st.Page("app_pages/carousel.py", title="Carousel", icon=":material/view_carousel:"),
            st.Page("app_pages/timeline.py", title="Timeline", icon=":material/timeline:"),
            st.Page("app_pages/pin_input.py", title="PinInput", icon=":material/pin:"),
        ],
        "i18n": [
            st.Page("app_pages/locale.py", title="Locale", icon=":material/translate:"),
        ],
    },
    position="sidebar",
)

# -- Header ------------------------------------------------------------------
_IS_DARK = st.context.theme.type == "dark"
_HEADER_GRADIENT = (
    "linear-gradient(135deg, #a78bfa, #ddd6fe)"
    if _IS_DARK
    else "linear-gradient(135deg, #7c3aed, #6d28d9)"
)
st.html(f"""
<div style="text-align:center; padding:1.5rem 0 0.5rem;">
    <h1 style="
        margin:0; font-size:2.5rem; font-weight:800;
        background:{_HEADER_GRADIENT};
        -webkit-background-clip:text; -webkit-text-fill-color:transparent;
        background-clip:text;
    ">st-rsuite</h1>
    <p style="margin:0.4rem 0 0; font-size:1rem; opacity:0.7;">
        RSuite date &amp; time components for Streamlit, powered by Components v2
    </p>
</div>
""")

# -- Sidebar: global controls -----------------------------------------------
with st.sidebar:
    st.session_state.disabled = st.toggle("Disable all components", value=False)
    st.divider()
    st.markdown(
        "**st-rsuite** brings RSuite's production-grade date & time components "
        "to Streamlit using the new Components v2 API. All components are MIT licensed."
    )

# -- Page title + run --------------------------------------------------------
st.title(f"{page.title}")
page.run()

# -- Footer ------------------------------------------------------------------
st.divider()
st.caption(
    "Built with [st-rsuite](https://github.com/lperezmo/st-rsuite) · "
    "Based on [RSuite](https://rsuitejs.com/) · "
    "Streamlit Components v2"
)
