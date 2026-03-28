<div align="center">
  <h1>st-rsuite</h1>
  <p>Built using <a href="https://rsuitejs.com/">RSuite</a> · Streamlit <a href="https://docs.streamlit.io/develop/api-reference/custom-components/st.components.v2.component">Components v2</a></p>

  <a href="https://pypi.org/project/st-rsuite/"><img src="https://img.shields.io/pypi/v/st-rsuite" alt="PyPI version"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-%E2%89%A53.10-blue" alt="Python >=3.10"></a>
  <a href="https://github.com/lperezmo/st-rsuite/blob/main/LICENSE"><img src="https://img.shields.io/github/license/lperezmo/st-rsuite" alt="License"></a>
  <a href="https://rsuite.streamlit.app/"><img src="https://static.streamlit.io/badges/streamlit_badge_black_white.svg" alt="Open in Streamlit"></a>
</div>

---

## Components

### Pickers — rich popups with full interaction

Calendar popups, scrolling time panels, range selection with hover highlighting — everything you'd expect from a production date/time picker.

| Component | Description | Streamlit equivalent |
|-----------|-------------|----------------------|
| `date_picker` | Calendar popup with format control, one-tap, ISO week | `st.date_input` |
| `date_range_picker` | Dual-calendar popup for date ranges, hover range | `st.date_input` (range mode) |
| `time_picker` | Time picker with scrolling panel, AM/PM | `st.time_input` |
| `time_range_picker` | Time range picker with dual panels | -- |

### Inputs — simple keyboard-only entry

Lightweight alternatives with no popup. Users navigate date segments with arrow keys and typing.

| Component | Description | Streamlit equivalent |
|-----------|-------------|----------------------|
| `date_input` | Keyboard-only date input (no popup) | `st.date_input` |
| `date_range_input` | Keyboard-only date range input (no popup) | `st.date_input` (range mode) |

### Selection

| Component | Description | Streamlit equivalent |
|-----------|-------------|----------------------|
| `radio_tile` | Tile-based radio group with icons and descriptions | `st.radio` |

### Tree — hierarchical data selection

| Component | Description | Streamlit equivalent |
|-----------|-------------|----------------------|
| `check_tree` | Standalone tree with checkboxes, searchable | -- |
| `check_tree_picker` | Dropdown picker with checkbox tree inside | `st.multiselect` (flat) |
| `multi_cascade_tree` | Multi-select cascading column navigation | -- |

### Display & Input

| Component | Description | Streamlit equivalent |
|-----------|-------------|----------------------|
| `carousel` | Content/image carousel with autoplay, local files & URLs | -- |
| `timeline` | Timeline with custom react-icons | -- |
| `pin_input` | PIN/verification code input with masking | `st.text_input` |

All components are **MIT licensed** (RSuite is fully open-source).

## Installation

```bash
uv add st-rsuite
```

or with pip:

```bash
pip install st-rsuite
```

## Quick start

```python
import streamlit as st
from datetime import date, time, timedelta
from st_rsuite import (
    date_picker, date_range_picker, time_picker,
    time_range_picker, date_input, date_range_input,
    radio_tile, check_tree, check_tree_picker,
    multi_cascade_tree, carousel, timeline, pin_input,
)

# ── Pickers ───────────────────────────────────────────────────────────────────

d = date_picker(label="Pick a date", value=date.today(), one_tap=True, key="my_dp")

start, end = date_range_picker(
    label="Trip dates",
    value=(date.today(), date.today() + timedelta(days=7)),
    hover_range="week",
    key="my_drp",
)

t = time_picker(
    label="Pick a time", value=time(9, 30),
    format="hh:mm aa", show_meridiem=True, key="my_tp",
)

t_start, t_end = time_range_picker(
    label="Shift hours",
    value=(time(9, 0), time(17, 0)),
    key="my_trp",
)

# ── Inputs ────────────────────────────────────────────────────────────────────

d2 = date_input(label="Type a date", value=date.today(), key="my_di")

start, end = date_range_input(
    label="Date range",
    value=(date.today(), date.today() + timedelta(days=7)),
    key="my_dri",
)

# ── Selection ─────────────────────────────────────────────────────────────────

selected = radio_tile(
    options=[
        {"value": "a", "label": "Option A", "description": "First option", "icon": "☀️"},
        {"value": "b", "label": "Option B", "description": "Second option", "icon": "🌙"},
    ],
    value="a",
    inline=True,
    key="my_tile",
)

# ── Tree components ───────────────────────────────────────────────────────────

tree_data = [
    {"value": "frontend", "label": "Frontend", "children": [
        {"value": "react", "label": "React"},
        {"value": "vue", "label": "Vue"},
    ]},
    {"value": "backend", "label": "Backend", "children": [
        {"value": "python", "label": "Python"},
        {"value": "go", "label": "Go"},
    ]},
]

checked = check_tree(data=tree_data, searchable=True, default_expand_all=True, key="my_ct")

picked = check_tree_picker(
    data=tree_data, placeholder="Select items", key="my_ctp",
)

cascade_data = [
    {"value": "us", "label": "US", "children": [
        {"value": "ca", "label": "California", "children": [
            {"value": "sf", "label": "San Francisco"},
        ]},
    ]},
]

cascade_selected = multi_cascade_tree(data=cascade_data, key="my_mct")

# ── Carousel ──────────────────────────────────────────────────────────────────

active = carousel(
    items=[
        {"content": "Slide 1", "background": "#7c3aed"},
        {"content": "Slide 2", "background": "#6d28d9"},
    ],
    autoplay=True,
    key="my_carousel",
)

# ── Timeline ──────────────────────────────────────────────────────────────────

timeline(
    items=[
        {"content": "Order placed", "time": "10:00", "icon": "FaCreditCard", "color": "#7c3aed"},
        {"content": "Shipped", "time": "14:30", "icon": "FaTruck", "color": "#0891b2"},
        {"content": "Delivered", "time": "11:30", "icon": "FaCheck", "color": "#059669"},
    ],
    align="left",
    key="my_timeline",
)

# ── PinInput ──────────────────────────────────────────────────────────────────

code = pin_input(length=6, mask=False, otp=True, key="my_pin")
```

## API

### Pickers

#### `date_picker`

```python
date_picker(
    label="",
    value=None,           # date object or YYYY-MM-DD string
    format="yyyy-MM-dd",
    appearance="default",  # 'default' | 'subtle'
    size="md",
    placeholder="",
    placement="bottomStart",
    one_tap=False,        # single-click select (no OK button)
    disabled=False,
    cleanable=True,
    block=False,          # full width
    iso_week=False,       # Monday-start weeks
    show_week_numbers=False,
    locale=None,          # e.g. 'ja_JP', 'zh_CN', 'es_ES'
    on_change=None,
    key=None,
) -> date | None
```

#### `date_range_picker`

```python
date_range_picker(
    label="",
    value=None,           # tuple of (date, date)
    format="yyyy-MM-dd",
    character=" ~ ",
    appearance="default",
    size="md",
    placeholder="",
    placement="bottomStart",
    disabled=False,
    cleanable=True,
    block=False,
    iso_week=False,
    show_week_numbers=False,
    show_one_calendar=False,  # single calendar panel
    one_tap=False,
    hover_range=None,     # 'week' | 'month' | None
    locale=None,
    on_change=None,
    key=None,
) -> tuple[date | None, date | None]
```

#### `time_picker`

```python
time_picker(
    label="",
    value=None,           # time object or HH:MM string
    format="HH:mm",       # 'HH:mm', 'HH:mm:ss', 'hh:mm aa'
    appearance="default",
    size="md",
    placeholder="",
    placement="bottomStart",
    disabled=False,
    cleanable=True,
    block=False,
    show_meridiem=False,  # AM/PM toggle
    locale=None,
    on_change=None,
    key=None,
) -> time | None
```

#### `time_range_picker`

```python
time_range_picker(
    label="",
    value=None,           # tuple of (time, time)
    format="HH:mm",
    character=" ~ ",
    appearance="default",
    size="md",
    placeholder="",
    placement="bottomStart",
    disabled=False,
    cleanable=True,
    block=False,
    show_meridiem=False,
    locale=None,
    on_change=None,
    key=None,
) -> tuple[time | None, time | None]
```

### Inputs

Simple keyboard-only components — no popups, designed for compact quick-entry scenarios.

#### `date_input`

```python
date_input(
    label="",
    value=None,           # date object or YYYY-MM-DD string
    format="yyyy-MM-dd",
    size="md",
    placeholder=None,
    disabled=False,
    locale=None,
    on_change=None,
    key=None,
) -> date | None
```

#### `date_range_input`

```python
date_range_input(
    label="",
    value=None,           # tuple of (date, date) or (str, str)
    format="yyyy-MM-dd",
    character=" ~ ",      # separator between start and end
    size="md",
    placeholder=None,
    disabled=False,
    locale=None,
    on_change=None,
    key=None,
) -> tuple[date | None, date | None]
```

### Selection

#### `radio_tile`

```python
radio_tile(
    options=[...],        # list of dicts: {value, label, description?, icon?}
    value=None,           # default selected value
    inline=False,         # horizontal layout
    disabled=False,
    locale=None,
    on_change=None,
    key=None,
) -> str | None
```

### Tree / Hierarchical

#### `check_tree`

```python
check_tree(
    data=[...],           # [{value, label, children?: [...]}]
    value=None,           # list of selected values
    cascade=True,         # parent/child cascade selection
    searchable=True,      # show search input
    default_expand_all=False,
    show_indent_line=False,
    height=360,           # tree height in px
    disabled=False,
    uncheckable_values=None,
    locale=None,
    on_change=None,
    key=None,
) -> list[str]
```

#### `check_tree_picker`

```python
check_tree_picker(
    data=[...],           # [{value, label, children?: [...]}]
    value=None,           # list of selected values
    cascade=True,
    searchable=True,
    countable=True,       # show selected count in toggle
    appearance="default",
    size="md",
    placeholder="Select",
    placement="bottomStart",
    disabled=False,
    cleanable=True,
    block=False,
    default_expand_all=False,
    show_indent_line=False,
    height=320,
    uncheckable_values=None,
    locale=None,
    on_change=None,
    key=None,
) -> list[str]
```

#### `multi_cascade_tree`

```python
multi_cascade_tree(
    data=[...],           # [{value, label, children?: [...]}]
    value=None,           # list of selected values
    cascade=True,
    searchable=False,
    column_width=156,     # width of each cascade column
    column_height=320,    # height of each cascade column
    disabled=False,
    uncheckable_values=None,
    locale=None,
    on_change=None,
    key=None,
) -> list[str]
```

### Display & Input

#### `carousel`

```python
carousel(
    items=[...],          # [{content?, src?, alt?, background?, color?}]  # src: URL or local file path
    autoplay=True,
    autoplay_interval=4000,  # ms between slides
    placement="bottom",   # indicator: 'top' | 'bottom' | 'left' | 'right'
    shape="dot",          # indicator: 'dot' | 'bar'
    active_index=0,
    locale=None,
    on_change=None,
    key=None,
) -> int                  # active slide index
```

#### `timeline`

```python
timeline(
    items=[...],          # [{content, time?, icon?, color?}]
    align="left",         # 'left' | 'right' | 'alternate'
    endless=False,        # continuous timeline line
    locale=None,
    key=None,
) -> None                 # display-only
```

The `icon` field accepts react-icons names (e.g. `"FaCheck"`, `"FaTruck"`, `"MdEmail"`) or emoji strings as fallback. 150+ icons from Font Awesome 5 and Material Design are included.

#### `pin_input`

```python
pin_input(
    length=6,
    value="",
    mask=False,           # password-style masking
    type="number",        # 'number' | 'alphabetic' | 'alphanumeric'
    size="md",
    placeholder="",
    disabled=False,
    read_only=False,
    otp=False,            # one-time password autocomplete
    attached=False,       # remove spacing between fields
    locale=None,
    on_change=None,
    key=None,
) -> str                  # current PIN value
```

## Locale / i18n

All components accept a `locale` parameter to switch calendar labels, month/day names, and button text to the target language. RSuite ships 29 locales out of the box.

When `locale` is not set, the component automatically detects the browser's language (`navigator.language`) and uses the closest matching RSuite locale.

```python
from st_rsuite import date_picker

# Japanese
date_picker(label="日付を選択", locale="ja_JP", one_tap=True, key="jp")

# Chinese (Simplified)
date_picker(label="选择日期", locale="zh_CN", one_tap=True, key="cn")

# Spanish
date_picker(label="Elegir fecha", locale="es_ES", one_tap=True, key="es")
```

**Available locales:** `ar_EG`, `ca_ES`, `cs_CZ`, `da_DK`, `de_DE`, `en_GB`, `en_US`, `es_AR`, `es_ES`, `fa_IR`, `fi_FI`, `fr_FR`, `gu_IN`, `hu_HU`, `it_IT`, `ja_JP`, `kk_KZ`, `ko_KR`, `ne_NP`, `nl_NL`, `pl_PL`, `pt_BR`, `ru_RU`, `sv_SE`, `th_TH`, `tr_TR`, `uk_UA`, `zh_CN`, `zh_TW`

## Running the example

```bash
uv add st-rsuite
uv run streamlit run examples/showcase.py
```

## Development

```bash
# Clone and install
git clone https://github.com/lperezmo/st-rsuite.git
cd st-rsuite
uv sync --dev

# Build frontend
cd st_rsuite/frontend
npm install
npm run build
cd ../..

# Run showcase
uv run streamlit run examples/showcase.py
```

## Disclaimer

Full disclaimer: This project was built with the help of [Claude Opus 4.6](https://www.anthropic.com/claude) by [Anthropic](https://www.anthropic.com), using [Claude Code](https://claude.ai/code) and [streamlit/agent-skills](https://github.com/streamlit/agent-skills). It is heavily based on [st-mui](https://github.com/lperezmo/st-mui).

## License

MIT
