# CHANGELOG


## v0.3.2 (2026-03-29)

### Bug Fixes

- Separate demo version bump into its own CI job to avoid permission errors
  ([`dbf634f`](https://github.com/lperezmo/st-rsuite/commit/dbf634f0d1f5412ae6d213359adb74bd6b96c308))

The python-semantic-release action left .git files with different ownership, causing 'Permission
  denied' on COMMIT_EDITMSG in the bump step. Moving the bump to its own job with a fresh checkout
  fixes this. Also decouples bump from publish so a bump failure can never block PyPI publishing.


## v0.3.1 (2026-03-29)

### Bug Fixes

- Configure git identity for demo app version bump in CI
  ([`30ab02c`](https://github.com/lperezmo/st-rsuite/commit/30ab02c23adc6cb42b73f89115fb558e027c2c2b))


## v0.3.0 (2026-03-28)

### Chores

- Add automatically bumping versions of demo app part of the semantic release workflow
  ([`8e56349`](https://github.com/lperezmo/st-rsuite/commit/8e56349cdf89dbeb77006794594d47aa34fbb7ad))

### Features

- Add 7 new components — RadioTile, CheckTree, CheckTreePicker, MultiCascadeTree, Carousel,
  Timeline, PinInput
  ([`f611a35`](https://github.com/lperezmo/st-rsuite/commit/f611a3553a3cc654001f2ef842085580b2f27e6e))

New components: - RadioTile: tile-based radio group with icons and descriptions - CheckTree:
  standalone searchable tree with checkboxes - CheckTreePicker: dropdown picker with checkbox tree -
  MultiCascadeTree: multi-select cascading column navigation - Carousel: image/content carousel with
  autoplay, supports local files and URLs - Timeline: timeline display with 150+ react-icons (Font
  Awesome 5 + Material Design) - PinInput: PIN/verification code input with mask, OTP, and type
  filtering

Also includes: - Refactored showcase into multipage Streamlit app with 9 page modules - Added public
  domain art images for carousel demos - Updated README with full API docs for all 13 components


## v0.2.1 (2026-03-19)

### Bug Fixes

- Resolve subpackage shadowing that made all component imports return modules instead of functions
  ([`00ef45e`](https://github.com/lperezmo/st-rsuite/commit/00ef45eec65393b3faba3d339972facb8f05498c))

The lazy __getattr__ loader was never triggered because Python's import machinery registers
  subpackage directories as module attributes before __getattr__ is consulted. Now setattr
  overwrites the subpackage reference with the actual function on first access.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

### Chores

- Bump version requirement for demo app
  ([`f541ee6`](https://github.com/lperezmo/st-rsuite/commit/f541ee6d699841a31b9fb73d4e0ee44d8ab12d89))


## v0.2.0 (2026-03-19)

### Chores

- Added a links to rsuite everywhere, removed one tap on date range picker on example because
  tapping on it twice is annoying,
  ([`fdbca8a`](https://github.com/lperezmo/st-rsuite/commit/fdbca8a8f2053204c39ed9022c9d61f3ece60032))

- Enable one tap for date pickers because the okay button gets covered by the streamlit cloud logo
  on the bottom right. also added disclaimer on time pickers and time range picker that okay button
  gets covered by hosted with streamlit cloud logo
  ([`f63e565`](https://github.com/lperezmo/st-rsuite/commit/f63e565a9eeb9e5511178068c7cf8f8e3711b1ad))

- Switch examples to requirements.txt for Streamlit Cloud
  ([`47a0e3a`](https://github.com/lperezmo/st-rsuite/commit/47a0e3a30f5d35abc1dbb838413b1c74f0a18366))

Streamlit Cloud uses Poetry internally and tried to install the pyproject.toml as a package. A plain
  requirements.txt avoids this.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>

### Features

- Add locale support with browser auto-detection
  ([`56f1d5e`](https://github.com/lperezmo/st-rsuite/commit/56f1d5e24c6f4240c1a9fa26a0b7367707651c1a))

Add `locale` parameter to all 6 components (29 RSuite locales). When unset, automatically detects
  browser language via navigator.language. Also exposes `__version__` via lazy imports and adds
  locale showcase tab.


## v0.1.0 (2026-03-19)

### Features

- Initial release of st-rsuite
  ([`902b240`](https://github.com/lperezmo/st-rsuite/commit/902b24039a8f5589841522b6f2da72354f65c5e2))

RSuite v6.1.2 date & time components for Streamlit (Components v2). Six components: DatePicker,
  DateRangePicker, TimePicker, TimeRangePicker, DateInput, and DateRangeInput. Includes Vite build
  pipeline, CI/CD with python-semantic-release, and interactive showcase app.

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
