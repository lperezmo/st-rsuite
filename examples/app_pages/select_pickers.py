import streamlit as st

from st_rsuite import check_picker, select_picker, tag_picker

from utils.ui import banner_rsuite, banner_st

disabled = st.session_state.get("disabled", False)

st.markdown(
    "Searchable dropdown pickers: single select with grouping, a "
    "multi-select rendered as removable tags that can create new options, "
    "and a checkbox multi-select with a selection count."
)

FRAMEWORKS = [
    {"value": "react", "label": "React", "group": "Frontend"},
    {"value": "vue", "label": "Vue", "group": "Frontend"},
    {"value": "angular", "label": "Angular", "group": "Frontend"},
    {"value": "django", "label": "Django", "group": "Backend"},
    {"value": "fastapi", "label": "FastAPI", "group": "Backend"},
    {"value": "rails", "label": "Rails", "group": "Backend"},
    {"value": "postgres", "label": "PostgreSQL", "group": "Database"},
    {"value": "mongodb", "label": "MongoDB", "group": "Database"},
]

# -- SelectPicker --------------------------------------------------------------
st.subheader("SelectPicker")
st.markdown(
    "A searchable single-select dropdown. Options group automatically when "
    "items carry a `group` key. Compare with `st.selectbox`, which has no "
    "grouping or disabled options."
)

st.markdown("#### Side by side")

col_rs, col_st = st.columns(2)
with col_rs:
    banner_rsuite()
    sp = select_picker(
        items=FRAMEWORKS,
        value="react",
        label="Framework",
        help="Grouped, searchable, with a disabled option",
        disabled_items=["rails"],
        block=True,
        disabled=disabled,
        key="sp_basic",
    )
    st.code(f"Selected: {sp}")
with col_st:
    banner_st()
    sb = st.selectbox(
        "Framework",
        options=[f["label"] for f in FRAMEWORKS],
        disabled=disabled,
        key="sb_basic",
    )
    st.code(f"Selected: {sb}")

st.divider()

st.markdown("#### Virtualized large list")
st.markdown(
    "With `virtualized=True` the dropdown renders thousands of options "
    "without slowing down. Try searching."
)

banner_rsuite()
big = select_picker(
    items=[{"value": f"item-{i}", "label": f"Item {i:04d}"} for i in range(2000)],
    virtualized=True,
    placeholder="Search 2,000 items",
    block=True,
    disabled=disabled,
    key="sp_virtualized",
)
st.code(f"Selected: {big}")

with st.expander("Usage code", icon=":material/code:"):
    st.code(
        """from st_rsuite import select_picker

items = [
    {"value": "react", "label": "React", "group": "Frontend"},
    {"value": "vue", "label": "Vue", "group": "Frontend"},
    {"value": "django", "label": "Django", "group": "Backend"},
]

selected = select_picker(
    items=items,                 # grouping turns on automatically
    value="react",
    label="Framework",
    disabled_items=["vue"],      # visible but not selectable
    virtualized=True,            # for very large lists
    key="my_select",
)""",
        language="python",
    )

# -- TagPicker -----------------------------------------------------------------
st.divider()
st.subheader("TagPicker")
st.markdown(
    "A searchable multi-select rendered as removable tags. With "
    "`creatable=True` users can add options that are not in the list, "
    "which `st.multiselect` only gained recently via `accept_new_options`."
)

st.markdown("#### Side by side")

col_rs2, col_st2 = st.columns(2)
with col_rs2:
    banner_rsuite()
    tp = tag_picker(
        items=FRAMEWORKS,
        value=["react", "postgres"],
        label="Stack",
        help="Type a value not in the list to create it",
        creatable=True,
        block=True,
        disabled=disabled,
        key="tp_basic",
    )
    st.code(f"Selected: {tp}")
with col_st2:
    banner_st()
    ms = st.multiselect(
        "Stack",
        options=[f["label"] for f in FRAMEWORKS],
        default=["React", "PostgreSQL"],
        disabled=disabled,
        key="ms_basic",
    )
    st.code(f"Selected: {ms}")

st.divider()

st.markdown("#### Grouped, with disabled options")

banner_rsuite()
tp2 = tag_picker(
    items=FRAMEWORKS,
    value=["fastapi"],
    disabled_items=["angular", "rails"],
    placeholder="Pick your stack",
    block=True,
    disabled=disabled,
    key="tp_grouped",
)
st.code(f"Selected: {tp2}")

with st.expander("Usage code", icon=":material/code:"):
    st.code(
        """from st_rsuite import tag_picker

items = [
    {"value": "react", "label": "React", "group": "Frontend"},
    {"value": "django", "label": "Django", "group": "Backend"},
]

selected = tag_picker(
    items=items,
    value=["react"],
    label="Stack",
    creatable=True,        # let users add values not in items
    key="my_tags",
)""",
        language="python",
    )

# -- CheckPicker ----------------------------------------------------------------
st.divider()
st.subheader("CheckPicker")
st.markdown(
    "A searchable multi-select with a checkbox per option. The closed control "
    "shows a selection count instead of one tag per value, so it stays tidy "
    "when many options are checked."
)

st.markdown("#### Side by side")

col_rs3, col_st3 = st.columns(2)
with col_rs3:
    banner_rsuite()
    ckp = check_picker(
        items=FRAMEWORKS,
        value=["react", "postgres"],
        label="Stack",
        help="Check as many options as you need",
        disabled_items=["rails"],
        block=True,
        disabled=disabled,
        key="ckp_basic",
    )
    st.code(f"Selected: {ckp}")
with col_st3:
    banner_st()
    ms2 = st.multiselect(
        "Stack",
        options=[f["label"] for f in FRAMEWORKS],
        default=["React", "PostgreSQL"],
        disabled=disabled,
        key="ms_basic_2",
    )
    st.code(f"Selected: {ms2}")

st.divider()

st.markdown("#### Grouped, with disabled options")

banner_rsuite()
ckp2 = check_picker(
    items=FRAMEWORKS,
    value=["fastapi"],
    disabled_items=["angular"],
    placeholder="Pick your stack",
    block=True,
    disabled=disabled,
    key="ckp_grouped",
)
st.code(f"Selected: {ckp2}")

with st.expander("Usage code", icon=":material/code:"):
    st.code(
        """from st_rsuite import check_picker

items = [
    {"value": "react", "label": "React", "group": "Frontend"},
    {"value": "django", "label": "Django", "group": "Backend"},
]

selected = check_picker(
    items=items,
    value=["react"],
    label="Stack",
    countable=True,          # show "N selected" in the closed control
    disabled_items=["django"],
    key="my_checks",
)""",
        language="python",
    )
