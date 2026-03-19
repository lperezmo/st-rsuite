"""st-rsuite: RSuite date & time components for Streamlit, built with Components v2."""

from importlib.metadata import version as _version

__version__ = _version("st-rsuite")

# Lazy imports — component registration requires `streamlit run` context,
# so we defer to allow `st_rsuite.__version__` from a plain Python shell.
def __getattr__(name: str):
    _imports = {
        "date_picker": "st_rsuite.date_picker",
        "date_range_picker": "st_rsuite.date_range_picker",
        "time_picker": "st_rsuite.time_picker",
        "time_range_picker": "st_rsuite.time_range_picker",
        "date_input": "st_rsuite.date_input",
        "date_range_input": "st_rsuite.date_range_input",
    }
    if name in _imports:
        from importlib import import_module
        return getattr(import_module(_imports[name]), name)
    raise AttributeError(f"module 'st_rsuite' has no attribute {name!r}")

__all__ = [
    "__version__",
    "date_picker",
    "date_range_picker",
    "time_picker",
    "time_range_picker",
    "date_input",
    "date_range_input",
]
