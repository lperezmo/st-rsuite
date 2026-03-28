"""Shared UI helpers — banners and header for the showcase app."""

import streamlit as st

_IS_DARK = st.context.theme.type == "dark"

# -- Branded column banners --------------------------------------------------

_RSUITE_BANNER_LIGHT = """
<div style="
    background: linear-gradient(135deg, #7c3aed 0%, #a78bfa 100%);
    color: white;
    padding: 0.55rem 1rem;
    border-radius: 0.5rem;
    margin-bottom: 0.75rem;
    font-weight: 600;
    font-size: 0.85rem;
    display: flex; align-items: center; gap: 0.5rem;
    box-shadow: 0 2px 8px rgba(124,58,237,0.25);
">&#9670; st-rsuite</div>
"""

_RSUITE_BANNER_DARK = """
<div style="
    background: linear-gradient(135deg, #6d28d9 0%, #8b5cf6 100%);
    color: white;
    padding: 0.55rem 1rem;
    border-radius: 0.5rem;
    margin-bottom: 0.75rem;
    font-weight: 600;
    font-size: 0.85rem;
    display: flex; align-items: center; gap: 0.5rem;
    box-shadow: 0 2px 12px rgba(124,58,237,0.35);
">&#9670; st-rsuite</div>
"""

_ST_BANNER_LIGHT = """
<div style="
    background: linear-gradient(135deg, #64748b 0%, #94a3b8 100%);
    color: white;
    padding: 0.55rem 1rem;
    border-radius: 0.5rem;
    margin-bottom: 0.75rem;
    font-weight: 600;
    font-size: 0.85rem;
    display: flex; align-items: center; gap: 0.5rem;
    box-shadow: 0 2px 8px rgba(100,116,139,0.25);
">&#9671; Streamlit built-in</div>
"""

_ST_BANNER_DARK = """
<div style="
    background: linear-gradient(135deg, #475569 0%, #64748b 100%);
    color: #e2e8f0;
    padding: 0.55rem 1rem;
    border-radius: 0.5rem;
    margin-bottom: 0.75rem;
    font-weight: 600;
    font-size: 0.85rem;
    display: flex; align-items: center; gap: 0.5rem;
    box-shadow: 0 2px 12px rgba(71,85,105,0.35);
">&#9671; Streamlit built-in</div>
"""


def banner_rsuite():
    st.html(_RSUITE_BANNER_DARK if _IS_DARK else _RSUITE_BANNER_LIGHT)


def banner_st():
    st.html(_ST_BANNER_DARK if _IS_DARK else _ST_BANNER_LIGHT)
