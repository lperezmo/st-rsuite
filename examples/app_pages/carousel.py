import streamlit as st
from pathlib import Path

from st_rsuite import carousel
from utils.ui import banner_rsuite

st.markdown(
    "A content carousel with autoplay, customizable indicators, "
    "and support for text or image slides. Works with **local files** and **URLs**."
)

# -- Resolve local image paths relative to this file -------------------------
_ASSETS = Path(__file__).parent.parent / "assets"

# -- Example 1: Local images -------------------------------------------------
st.subheader("Local images")
st.caption(
    "Pass local file paths via the `src` key. "
    "Great for bundled assets shipped with your app."
)

banner_rsuite()
ci_local = carousel(
    items=[
        {
            "src": str(_ASSETS / "starry_night.jpg"),
            "alt": "The Starry Night — Vincent van Gogh, 1889",
        },
        {
            "src": str(_ASSETS / "great_wave.jpg"),
            "alt": "The Great Wave off Kanagawa — Katsushika Hokusai, c. 1831",
        },
        {
            "src": str(_ASSETS / "girl_pearl_earring.jpg"),
            "alt": "Girl with a Pearl Earring — Johannes Vermeer, c. 1665",
        },
    ],
    autoplay=True,
    autoplay_interval=4000,
    key="car_local",
)
st.code(f"Active slide: {ci_local}")

with st.expander("Usage code", icon=":material/code:"):
    st.code(
        '''from st_rsuite import carousel
from pathlib import Path

ASSETS = Path(__file__).parent / "assets"

active = carousel(
    items=[
        {"src": str(ASSETS / "starry_night.jpg"), "alt": "Starry Night"},
        {"src": str(ASSETS / "great_wave.jpg"),   "alt": "Great Wave"},
        {"src": str(ASSETS / "pearl_earring.jpg"), "alt": "Pearl Earring"},
    ],
    autoplay=True,
    autoplay_interval=4000,
    key="my_carousel",
)''',
        language="python",
    )

# -- Example 2: URL images ---------------------------------------------------
st.divider()
st.subheader("URL images")
st.caption(
    "Pass any public image URL via the `src` key — no download needed. "
    "Perfect for remote assets, CDNs, or user-provided links."
)

banner_rsuite()
ci_url = carousel(
    items=[
        {
            "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/1280px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg",
            "alt": "The Starry Night — Van Gogh (via Wikimedia)",
        },
        {
            "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a5/Tsunami_by_hokusai_19th_century.jpg/1280px-Tsunami_by_hokusai_19th_century.jpg",
            "alt": "The Great Wave — Hokusai (via Wikimedia)",
        },
        {
            "src": "https://upload.wikimedia.org/wikipedia/commons/d/d7/Meisje_met_de_parel.jpg",
            "alt": "Girl with a Pearl Earring — Vermeer (via Wikimedia)",
        },
    ],
    autoplay=True,
    autoplay_interval=5000,
    shape="bar",
    key="car_url",
)
st.code(f"Active slide: {ci_url}")

with st.expander("Usage code", icon=":material/code:"):
    st.code(
        '''from st_rsuite import carousel

active = carousel(
    items=[
        {
            "src": "https://example.com/photo1.jpg",
            "alt": "Description of photo 1",
        },
        {
            "src": "https://example.com/photo2.jpg",
            "alt": "Description of photo 2",
        },
    ],
    autoplay=True,
    autoplay_interval=5000,
    shape="bar",
    key="my_url_carousel",
)''',
        language="python",
    )

# -- Example 3: Text slides --------------------------------------------------
st.divider()
st.subheader("Text slides")
st.caption("Use `content` + `background` for simple text-based slides — no images needed.")

banner_rsuite()
ci_text = carousel(
    items=[
        {"content": "Welcome to st-rsuite", "background": "#7c3aed"},
        {"content": "RSuite components for Streamlit", "background": "#6d28d9"},
        {"content": "Built with Components v2", "background": "#5b21b6"},
        {"content": "Fully MIT licensed", "background": "#4c1d95"},
    ],
    autoplay=True,
    autoplay_interval=3000,
    key="car_text",
)
st.code(f"Active slide: {ci_text}")

st.divider()

st.subheader("Bar indicators, left placement")

banner_rsuite()
ci_bar = carousel(
    items=[
        {"content": "Slide A", "background": "#059669"},
        {"content": "Slide B", "background": "#0891b2"},
        {"content": "Slide C", "background": "#d97706"},
    ],
    shape="bar",
    placement="left",
    autoplay=False,
    key="car_bar",
)
st.code(f"Active slide: {ci_bar}")

with st.expander("Usage code", icon=":material/code:"):
    st.code(
        '''from st_rsuite import carousel

active = carousel(
    items=[
        {"content": "Slide 1", "background": "#7c3aed"},
        {"content": "Slide 2", "background": "#6d28d9"},
        {"src": "https://example.com/image.jpg", "alt": "Photo"},
    ],
    autoplay=True,
    autoplay_interval=3000,
    shape="dot",       # "dot" or "bar"
    placement="bottom", # "top", "bottom", "left", "right"
    key="my_carousel",
)''',
        language="python",
    )
