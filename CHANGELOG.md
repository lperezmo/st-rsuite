# CHANGELOG


## v0.3.3 (2026-06-22)

### Bug Fixes

- Require Streamlit >= 1.53, add CCv2 e2e tests and CI
  ([#1](https://github.com/lperezmo/st-rsuite/pull/1),
  [`ecd49b0`](https://github.com/lperezmo/st-rsuite/commit/ecd49b079c5797360fa6f14d78a66e8bd4272d3f))

* fix: require Streamlit >= 1.53

st-rsuite components pass isolate_styles to st.components.v2.component(), and that option only
  exists in Streamlit 1.53 and newer. On older Streamlit the component cannot register, which
  surfaces as "Component 'st-rsuite.<name>' must be declared in pyproject.toml with asset_dir to use
  file-backed js" (or an isolate_styles TypeError). The package advertised streamlit>=1.51, so users
  on 1.51 and 1.52 hit this.

Raise the floor to streamlit>=1.53, keep the examples on the newest Streamlit, and document the
  requirement with a Requirements section, a Troubleshooting note, and a badge in the README. Also
  add a dev dependency group for the test suite.

* test: add CCv2 e2e and registration smoke suite

test/test_ccv2_e2e.py drives a real Streamlit server with Playwright and checks that all 13
  components mount a Components v2 node (never an iframe), render RSuite markup, and round-trip
  their values. test/test_registration_smoke.py is a fast, browser-less guard that mirrors the
  runtime startup discovery and asserts every component asset_dir resolves and isolate_styles is
  available.

streamlit.testing.v1.AppTest cannot test this: it never runs component discovery, so it reports
  every file-backed component as unregistered.

* ci: run the test suite across a Streamlit version matrix

Build the frontend once, run the smoke suite on every supported Streamlit minor (1.53 through
  latest), and run the Playwright e2e suite on 1.53, 1.55, and latest. A package job asserts the
  wheel ships the component manifest and built JS so a packaging regression that would break
  registration for everyone is caught.

### Chores

- Bump demo app requirement to v0.3.2
  ([`912b4e8`](https://github.com/lperezmo/st-rsuite/commit/912b4e887c1aa323eede71552dc655427e20b420))

- Remove faulty badge
  ([`16b63a1`](https://github.com/lperezmo/st-rsuite/commit/16b63a1175d4091a0a5a7bf6de90710a7844a498))

- Replace broken static.streamlit.io badge with shields.io
  ([`ff05dcc`](https://github.com/lperezmo/st-rsuite/commit/ff05dcc4f3596b93afbb77a2c8ba8e6bdfcdb8f7))


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
