"""st-rsuite: RSuite date & time components for Streamlit, built with Components v2."""

from importlib.metadata import version as _version

__version__ = _version("st-rsuite")

_COMPONENT_IMPORTS = {
    "date_picker": "st_rsuite.date_picker",
    "date_range_picker": "st_rsuite.date_range_picker",
    "time_picker": "st_rsuite.time_picker",
    "time_range_picker": "st_rsuite.time_range_picker",
    "date_input": "st_rsuite.date_input",
    "date_range_input": "st_rsuite.date_range_input",
    "radio_tile": "st_rsuite.radio_tile",
    "select_picker": "st_rsuite.select_picker",
    "tag_picker": "st_rsuite.tag_picker",
    "check_tree": "st_rsuite.check_tree",
    "check_tree_picker": "st_rsuite.check_tree_picker",
    "tree_picker": "st_rsuite.tree_picker",
    "cascader": "st_rsuite.cascader",
    "multi_cascade_tree": "st_rsuite.multi_cascade_tree",
    "carousel": "st_rsuite.carousel",
    "timeline": "st_rsuite.timeline",
    "pin_input": "st_rsuite.pin_input",
}


def __getattr__(name: str):
    if name in _COMPONENT_IMPORTS:
        import importlib
        import sys

        func = getattr(importlib.import_module(_COMPONENT_IMPORTS[name]), name)
        # Bind the function directly on this module so __getattr__ isn't
        # called again AND so it shadows the subpackage module reference.
        setattr(sys.modules[__name__], name, func)
        return func
    raise AttributeError(f"module 'st_rsuite' has no attribute {name!r}")


__all__ = [
    "__version__",
    "date_picker",
    "date_range_picker",
    "time_picker",
    "time_range_picker",
    "date_input",
    "date_range_input",
    "radio_tile",
    "select_picker",
    "tag_picker",
    "check_tree",
    "check_tree_picker",
    "tree_picker",
    "cascader",
    "multi_cascade_tree",
    "carousel",
    "timeline",
    "pin_input",
]
