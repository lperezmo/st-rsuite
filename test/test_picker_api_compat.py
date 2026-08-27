"""Regression tests for public picker call signatures."""

from inspect import signature

from st_rsuite.tag_picker import tag_picker


def test_tag_picker_keeps_legacy_positional_parameter_order():
    """A new option must not reinterpret existing positional arguments."""
    parameters = list(signature(tag_picker).parameters)
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
