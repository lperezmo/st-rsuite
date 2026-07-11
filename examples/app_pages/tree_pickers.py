import streamlit as st

from st_rsuite import cascader, tree_picker
from utils.data import CASCADE_DATA, TREE_DATA
from utils.ui import banner_rsuite

disabled = st.session_state.get("disabled", False)

st.markdown(
    "Single-select counterparts of the tree family: a cascading column "
    "picker and a dropdown tree. Both return one value (or None)."
)

# -- Cascader ------------------------------------------------------------------
st.subheader("Cascader")
st.markdown(
    "Navigate hierarchical levels column by column and pick ONE item. "
    "The single-select sibling of MultiCascadeTree."
)

st.markdown("#### Basic (leaf-only selection)")

banner_rsuite()
cas = cascader(
    data=CASCADE_DATA,
    label="City",
    help="Only leaf nodes (cities) are selectable",
    searchable=True,
    disabled=disabled,
    key="cas_basic",
)
st.code(f"Selected: {cas}")

st.divider()

st.markdown("#### Parents selectable, wide columns")
st.markdown(
    "With `parent_selectable=True` a country or state is a valid answer, "
    "not just a city."
)

banner_rsuite()
cas2 = cascader(
    data=CASCADE_DATA,
    value="ca",
    parent_selectable=True,
    column_width=220,
    disabled=disabled,
    key="cas_parents",
)
st.code(f"Selected: {cas2}")

with st.expander("Usage code", icon=":material/code:"):
    st.code(
        """from st_rsuite import cascader

data = [
    {"value": "us", "label": "United States", "children": [
        {"value": "ca", "label": "California", "children": [
            {"value": "sf", "label": "San Francisco"},
        ]},
    ]},
]

selected = cascader(
    data=data,
    label="City",
    parent_selectable=False,   # True lets non-leaf nodes be the answer
    searchable=True,
    key="my_cascader",
)""",
        language="python",
    )

# -- TreePicker ------------------------------------------------------------------
st.divider()
st.subheader("TreePicker")
st.markdown(
    "A dropdown with a single-select tree inside. The single-select "
    "sibling of CheckTreePicker."
)

st.markdown("#### Basic, expanded")

banner_rsuite()
tpv = tree_picker(
    data=TREE_DATA,
    label="Technology",
    default_expand_all=True,
    show_indent_line=True,
    disabled=disabled,
    key="tpv_basic",
)
st.code(f"Selected: {tpv}")

st.divider()

st.markdown("#### Leaf-only, with disabled items")
st.markdown(
    "`only_leaf_selectable=True` keeps categories unselectable; "
    "`disabled_items=` greys out specific options."
)

banner_rsuite()
tpv2 = tree_picker(
    data=TREE_DATA,
    value="react",
    only_leaf_selectable=True,
    disabled_items=["mongodb", "redis"],
    default_expand_all=True,
    disabled=disabled,
    key="tpv_leaf",
)
st.code(f"Selected: {tpv2}")

with st.expander("Usage code", icon=":material/code:"):
    st.code(
        """from st_rsuite import tree_picker

data = [
    {"value": "frontend", "label": "Frontend", "children": [
        {"value": "react", "label": "React"},
        {"value": "vue", "label": "Vue"},
    ]},
]

selected = tree_picker(
    data=data,
    label="Technology",
    default_expand_all=True,
    only_leaf_selectable=True,   # categories are not answers
    disabled_items=["vue"],
    key="my_tree_picker",
)""",
        language="python",
    )
