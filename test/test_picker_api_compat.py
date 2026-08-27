"""Regression tests for public picker call signatures."""

import ast
from pathlib import Path

TAG_PICKER_MODULE = (
    Path(__file__).parent.parent / "st_rsuite" / "tag_picker" / "__init__.py"
)


def test_tag_picker_keeps_legacy_positional_parameter_order():
    """A new option must not reinterpret existing positional arguments."""
    module = ast.parse(TAG_PICKER_MODULE.read_text(encoding="utf-8"))
    function = next(
        node
        for node in module.body
        if isinstance(node, ast.FunctionDef) and node.name == "tag_picker"
    )
    parameters = [argument.arg for argument in function.args.args]
    legacy_tail = [
        "size",
        "placeholder",
        "placement",
        "disabled",
        "cleanable",
        "block",
        "loading",
        "help",
        "locale",
        "on_change",
        "key",
    ]
    start = parameters.index("disabled_items") + 1
    assert parameters[start : start + len(legacy_tail)] == legacy_tail
    assert parameters[-1] == "appearance"
