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

These are the main attraction. Calendar popups, scrolling time panels, range selection with hover highlighting — everything you'd expect from a production date/time picker.

| Component | Description | Streamlit equivalent |
|-----------|-------------|----------------------|
| `date_picker` | Calendar popup with format control, one-tap, ISO week | `st.date_input` |
| `date_range_picker` | Dual-calendar popup for date ranges, hover range | `st.date_input` (range mode) |
| `time_picker` | Time picker with scrolling panel, AM/PM | `st.time_input` |
| `time_range_picker` | Time range picker with dual panels | -- |

### Inputs — simple keyboard-only entry

Lightweight alternatives with no popup. Users navigate date segments with arrow keys and typing — useful for compact forms where a full picker would be overkill.

| Component | Description | Streamlit equivalent |
|-----------|-------------|----------------------|
| `date_input` | Keyboard-only date input (no popup) | `st.date_input` |
| `date_range_input` | Keyboard-only date range input (no popup) | `st.date_input` (range mode) |

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
)

# ── Pickers — the star of the show ──────────────────────────────────────────

# Calendar popup with one-tap selection
d = date_picker(label="Pick a date", value=date.today(), one_tap=True, key="my_dp")

# Dual-calendar range picker with week hover highlighting
start, end = date_range_picker(
    label="Trip dates",
    value=(date.today(), date.today() + timedelta(days=7)),
    hover_range="week",
    key="my_drp",
)

# Time picker with AM/PM
t = time_picker(
    label="Pick a time", value=time(9, 30),
    format="hh:mm aa", show_meridiem=True, key="my_tp",
)

# Time range — great for scheduling
t_start, t_end = time_range_picker(
    label="Shift hours",
    value=(time(9, 0), time(17, 0)),
    key="my_trp",
)

# ── Inputs — simple keyboard-only entry (no popups) ─────────────────────────

d2 = date_input(label="Type a date", value=date.today(), key="my_di")

start, end = date_range_input(
    label="Date range",
    value=(date.today(), date.today() + timedelta(days=7)),
    key="my_dri",
)
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
    locale=None,          # e.g. 'ja_JP', 'zh_CN', 'es_ES'
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
    locale=None,          # e.g. 'ja_JP', 'zh_CN', 'es_ES'
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
    locale=None,          # e.g. 'ja_JP', 'zh_CN', 'es_ES'
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
    format="yyyy-MM-dd",  # Unicode date format tokens
    size="md",            # 'lg' | 'md' | 'sm' | 'xs'
    placeholder=None,
    disabled=False,
    locale=None,          # e.g. 'ja_JP', 'zh_CN', 'es_ES'
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
    locale=None,          # e.g. 'ja_JP', 'zh_CN', 'es_ES'
    on_change=None,
    key=None,
) -> tuple[date | None, date | None]
```

## Locale / i18n

All components accept a `locale` parameter to switch calendar labels, month/day names, and button text to the target language. RSuite ships 29 locales out of the box.

When `locale` is not set, the component automatically detects the browser's language (`navigator.language`) and uses the closest matching RSuite locale. For example, a browser set to Japanese will show Japanese calendar labels without any code changes.

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
