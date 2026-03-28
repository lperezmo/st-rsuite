import streamlit as st

from st_rsuite import check_tree, check_tree_picker, multi_cascade_tree
from utils.ui import banner_rsuite
from utils.data import TREE_DATA, PICKER_DATA, CASCADE_DATA

disabled = st.session_state.get("disabled", False)

st.markdown("Hierarchical selection components: standalone trees, dropdown pickers, and cascading columns.")

# -- CheckTree ---------------------------------------------------------------
st.subheader("CheckTree")
st.markdown(
    "A standalone tree with checkboxes for multi-selection. "
    "Supports cascade selection, search, and indent lines."
)

st.markdown("#### Basic with search")

banner_rsuite()
ct = check_tree(
    data=TREE_DATA,
    value=["react", "python"],
    searchable=True,
    default_expand_all=True,
    disabled=disabled,
    key="ct_basic",
)
st.code(f"Selected: {ct}")

st.divider()

st.markdown("#### With indent lines, no cascade")

banner_rsuite()
ct2 = check_tree(
    data=TREE_DATA,
    cascade=False,
    searchable=True,
    default_expand_all=True,
    show_indent_line=True,
    disabled=disabled,
    key="ct_indent",
)
st.code(f"Selected: {ct2}")

with st.expander("Usage code", icon=":material/code:"):
    st.code(
        '''from st_rsuite import check_tree

data = [
    {"value": "root", "label": "Root", "children": [
        {"value": "frontend", "label": "Frontend", "children": [
            {"value": "react", "label": "React"},
            {"value": "vue", "label": "Vue"},
        ]},
        {"value": "backend", "label": "Backend", "children": [
            {"value": "python", "label": "Python"},
            {"value": "go", "label": "Go"},
        ]},
    ]}
]

selected = check_tree(
    data=data,
    value=["react"],
    searchable=True,
    default_expand_all=True,
    key="my_tree",
)''',
        language="python",
    )

# -- CheckTreePicker ---------------------------------------------------------
st.divider()
st.subheader("CheckTreePicker")
st.markdown(
    "A dropdown picker with a checkbox tree inside. "
    "Compact way to select from hierarchical data."
)

st.markdown("#### Basic")

banner_rsuite()
ctp = check_tree_picker(
    data=PICKER_DATA,
    value=["alice", "bob"],
    placeholder="Select team members",
    disabled=disabled,
    key="ctp_basic",
)
st.code(f"Selected: {ctp}")

st.divider()

st.markdown("#### Expanded, with indent lines")

banner_rsuite()
ctp2 = check_tree_picker(
    data=PICKER_DATA,
    default_expand_all=True,
    show_indent_line=True,
    block=True,
    disabled=disabled,
    key="ctp_expanded",
)
st.code(f"Selected: {ctp2}")

with st.expander("Usage code", icon=":material/code:"):
    st.code(
        '''from st_rsuite import check_tree_picker

data = [
    {"value": "eng", "label": "Engineering", "children": [
        {"value": "alice", "label": "Alice"},
        {"value": "bob", "label": "Bob"},
    ]},
    {"value": "design", "label": "Design", "children": [
        {"value": "carol", "label": "Carol"},
    ]},
]

selected = check_tree_picker(
    data=data,
    value=["alice"],
    placeholder="Select team members",
    key="my_picker",
)''',
        language="python",
    )

# -- MultiCascadeTree --------------------------------------------------------
st.divider()
st.subheader("MultiCascadeTree")
st.markdown(
    "A multi-select cascading tree with column-based navigation. "
    "Navigate through hierarchical levels and check multiple items."
)

st.markdown("#### Basic")

banner_rsuite()
mct = multi_cascade_tree(
    data=CASCADE_DATA,
    value=["sf", "nyc"],
    disabled=disabled,
    key="mct_basic",
)
st.code(f"Selected: {mct}")

st.divider()

st.markdown("#### Wide columns, no cascade")

banner_rsuite()
mct2 = multi_cascade_tree(
    data=CASCADE_DATA,
    cascade=False,
    column_width=200,
    disabled=disabled,
    key="mct_wide",
)
st.code(f"Selected: {mct2}")

with st.expander("Usage code", icon=":material/code:"):
    st.code(
        '''from st_rsuite import multi_cascade_tree

data = [
    {"value": "us", "label": "United States", "children": [
        {"value": "ca", "label": "California", "children": [
            {"value": "sf", "label": "San Francisco"},
            {"value": "la", "label": "Los Angeles"},
        ]},
        {"value": "ny", "label": "New York", "children": [
            {"value": "nyc", "label": "New York City"},
        ]},
    ]},
]

selected = multi_cascade_tree(
    data=data,
    value=["sf"],
    key="my_cascade",
)''',
        language="python",
    )
