"""Regression guards for security-sensitive showcase output."""

from __future__ import annotations

import ast
from pathlib import Path

SENSITIVE_VALUES = {"pi2", "pi4"}
VISIBLE_STREAMLIT_SINKS = {"code", "html", "markdown", "text", "write"}


def test_masked_pin_and_otp_are_not_echoed_verbatim():
    source_path = (
        Path(__file__).parent.parent / "examples" / "app_pages" / "pin_input.py"
    )
    tree = ast.parse(source_path.read_text())

    for call in (node for node in ast.walk(tree) if isinstance(node, ast.Call)):
        func = call.func
        if not (
            isinstance(func, ast.Attribute)
            and isinstance(func.value, ast.Name)
            and func.value.id == "st"
            and func.attr in VISIBLE_STREAMLIT_SINKS
        ):
            continue

        for argument in call.args:
            assert not (
                isinstance(argument, ast.Name) and argument.id in SENSITIVE_VALUES
            ), f"{argument.id} is rendered directly by st.{func.attr}"
            if not isinstance(argument, ast.JoinedStr):
                continue
            for part in argument.values:
                assert not (
                    isinstance(part, ast.FormattedValue)
                    and isinstance(part.value, ast.Name)
                    and part.value.id in SENSITIVE_VALUES
                ), f"{part.value.id} is interpolated directly by st.{func.attr}"
