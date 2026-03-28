"""RSuite Timeline component for Streamlit."""

from __future__ import annotations

import streamlit as st

_component = st.components.v2.component(
    "st-rsuite.timeline",
    js="index-*.js",
    html='<div class="react-root"></div>',
    isolate_styles=False,
)


def timeline(
    items: list[dict],
    align: str = "left",
    endless: bool = False,
    locale: str | None = None,
    key: str | None = None,
) -> None:
    """A timeline display powered by RSuite with custom icon support.

    Parameters
    ----------
    items : list of dict
        Timeline entries. Each dict can have:
        - 'content' (str, required): main text content
        - 'time' (str, optional): time label
        - 'icon' (str, optional): icon name from react-icons registry
          (e.g. 'FaCheck', 'FaTruck', 'MdEmail') or an emoji string
        - 'color' (str, optional): icon/dot color
    align : str
        Timeline alignment: 'left', 'right', or 'alternate'.
    endless : bool
        Show continuous timeline line.
    locale : str or None
        RSuite locale key.
    key : str or None
        Unique widget key.

    Returns
    -------
    None
        Display-only component.

    Available icon names (curated subset)
    -------------------------------------
    Font Awesome: FaCheck, FaTimes, FaUser, FaHome, FaCog, FaBell,
    FaEnvelope, FaStar, FaHeart, FaTruck, FaPlane, FaRocket, FaCreditCard,
    FaShoppingCart, FaCode, FaBug, FaDatabase, FaServer, FaChartLine,
    FaCalendar, FaClock, FaMapMarkerAlt, FaFlag, FaTrophy, FaGithub, ...

    Material Design: MdHome, MdSearch, MdSettings, MdEmail, MdPerson,
    MdStar, MdFavorite, MdEdit, MdDelete, MdCheckCircle, MdInfo,
    MdWarning, MdError, MdDashboard, MdTimeline, MdAnalytics, ...
    """

    def _noop():
        pass

    _component(
        key=key,
        default={"_nonce": 0},
        data={
            "items": items,
            "align": align,
            "endless": endless,
            "locale": locale,
        },
        on__nonce_change=_noop,
    )
