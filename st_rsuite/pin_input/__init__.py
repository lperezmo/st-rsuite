"""RSuite PinInput component for Streamlit."""

from __future__ import annotations

from typing import Callable

import streamlit as st

_component = st.components.v2.component(
    "st-rsuite.pin_input",
    js="index-*.js",
    html='<div class="react-root"></div>',
    isolate_styles=False,
)


def pin_input(
    length: int = 6,
    value: str = "",
    mask: bool = False,
    type: str = "number",
    size: str = "md",
    placeholder: str = "",
    disabled: bool = False,
    read_only: bool = False,
    otp: bool = False,
    attached: bool = False,
    locale: str | None = None,
    on_change: Callable | None = None,
    key: str | None = None,
) -> str:
    """A PIN/verification code input powered by RSuite.

    Parameters
    ----------
    length : int
        Number of input fields (default 6).
    value : str
        Default PIN value.
    mask : bool
        Mask input like a password.
    type : str
        Input type: 'number', 'alphabetic', or 'alphanumeric'.
    size : str
        Component size: 'lg', 'md', 'sm', or 'xs'.
    placeholder : str
        Placeholder character.
    disabled : bool
        Disable the component.
    read_only : bool
        Read-only mode.
    otp : bool
        Optimize for one-time password (sets autocomplete).
    attached : bool
        Remove spacing between input fields.
    locale : str or None
        RSuite locale key.
    on_change : callable or None
        Callback when the PIN value changes.
    key : str or None
        Unique widget key.

    Returns
    -------
    str
        The current PIN value.
    """

    def _noop():
        pass

    result = _component(
        key=key,
        default={"pin_value": value},
        data={
            "length": length,
            "value": value,
            "mask": mask,
            "type": type,
            "size": size,
            "placeholder": placeholder,
            "disabled": disabled,
            "readOnly": read_only,
            "otp": otp,
            "attached": attached,
            "locale": locale,
        },
        on_pin_value_change=on_change or _noop,
    )

    val = result.get("pin_value") if result else ""
    return val if val else ""
