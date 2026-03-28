import streamlit as st

from st_rsuite import timeline
from utils.ui import banner_rsuite

st.markdown(
    "A timeline display with custom icons from react-icons. "
    "Supports left, right, and alternate alignment."
)

st.markdown("#### Order tracking with icons")

banner_rsuite()
timeline(
    items=[
        {"content": "Order placed", "time": "2026-03-20 10:00", "icon": "FaCreditCard", "color": "#7c3aed"},
        {"content": "Payment confirmed", "time": "2026-03-20 10:05", "icon": "FaCheckCircle", "color": "#059669"},
        {"content": "Shipped from warehouse", "time": "2026-03-21 14:30", "icon": "FaTruck", "color": "#0891b2"},
        {"content": "In transit", "time": "2026-03-22 09:00", "icon": "FaPlane", "color": "#d97706"},
        {"content": "Out for delivery", "time": "2026-03-23 08:00", "icon": "FaWalking", "color": "#6d28d9"},
        {"content": "Delivered!", "time": "2026-03-23 11:30", "icon": "FaCheck", "color": "#059669"},
    ],
    key="tl_order",
)

st.divider()

st.markdown("#### Alternate alignment with mixed icons")

banner_rsuite()
timeline(
    items=[
        {"content": "Project kickoff", "time": "Jan 2026", "icon": "FaRocket", "color": "#7c3aed"},
        {"content": "Design phase", "time": "Feb 2026", "icon": "FaPalette", "color": "#ec4899"},
        {"content": "Development sprint", "time": "Mar 2026", "icon": "FaCode", "color": "#0891b2"},
        {"content": "Testing & QA", "time": "Apr 2026", "icon": "FaBug", "color": "#d97706"},
        {"content": "Launch!", "time": "May 2026", "icon": "FaStar", "color": "#059669"},
    ],
    align="alternate",
    key="tl_alternate",
)

st.divider()

st.markdown("#### Material Design icons + emoji fallback")

banner_rsuite()
timeline(
    items=[
        {"content": "User signed up", "time": "9:00 AM", "icon": "MdPerson"},
        {"content": "Email verified", "time": "9:05 AM", "icon": "MdEmail"},
        {"content": "Profile completed", "time": "9:15 AM", "icon": "MdCheckCircle", "color": "#059669"},
        {"content": "First purchase", "time": "10:30 AM", "icon": "\U0001F389"},
    ],
    key="tl_material",
)

with st.expander("Usage code", icon=":material/code:"):
    st.code(
        '''from st_rsuite import timeline

timeline(
    items=[
        {"content": "Step 1", "time": "10:00", "icon": "FaCheck", "color": "#059669"},
        {"content": "Step 2", "time": "11:00", "icon": "FaTruck", "color": "#0891b2"},
        {"content": "Step 3", "time": "12:00", "icon": "\\U0001F389"},  # emoji fallback
    ],
    align="left",   # "left", "right", or "alternate"
    endless=False,
    key="my_timeline",
)

# Available icons: FaCheck, FaTruck, FaPlane, FaRocket, FaCreditCard,
# FaCode, FaBug, FaStar, MdEmail, MdPerson, MdCheckCircle, ...
# See timeline() docstring for full list.''',
        language="python",
    )
