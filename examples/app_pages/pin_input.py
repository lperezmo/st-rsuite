import streamlit as st

from st_rsuite import pin_input
from utils.ui import banner_rsuite

disabled = st.session_state.get("disabled", False)

st.markdown(
    "A PIN / verification code input with configurable length, "
    "masking, and input type filtering."
)

st.markdown("#### Basic (6-digit)")

banner_rsuite()
pi = pin_input(
    length=6,
    disabled=disabled,
    key="pi_basic",
)
st.code(f"PIN: '{pi}'")

st.divider()

st.markdown("#### 4-digit masked (password style)")

banner_rsuite()
pi2 = pin_input(
    length=4,
    mask=True,
    disabled=disabled,
    key="pi_masked",
)
st.code(f"PIN: '{pi2}'")

st.divider()

st.markdown("#### Alphanumeric, attached style")

banner_rsuite()
pi3 = pin_input(
    length=6,
    type="alphanumeric",
    attached=True,
    size="lg",
    disabled=disabled,
    key="pi_alpha",
)
st.code(f"Code: '{pi3}'")

st.divider()

st.markdown("#### OTP mode")

banner_rsuite()
pi4 = pin_input(
    length=6,
    otp=True,
    placeholder="\u2022",
    disabled=disabled,
    key="pi_otp",
)
st.code(f"OTP: '{pi4}'")

with st.expander("Usage code", icon=":material/code:"):
    st.code(
        '''from st_rsuite import pin_input

code = pin_input(
    length=6,
    mask=False,
    type="number",       # "number", "alphabetic", or "alphanumeric"
    size="md",           # "lg", "md", "sm", "xs"
    otp=True,            # optimized for one-time passwords
    attached=False,      # remove spacing between fields
    key="my_pin",
)''',
        language="python",
    )
