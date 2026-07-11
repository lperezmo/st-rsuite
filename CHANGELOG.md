# CHANGELOG


## v0.9.0 (2026-07-11)

### Chores

- Bump demo app requirement to v0.8.0
  ([`9a220eb`](https://github.com/lperezmo/st-rsuite/commit/9a220ebe196cd4674daee02b035470f664f05456))

### Features

- Cascader and tree_picker
  ([`9cd0054`](https://github.com/lperezmo/st-rsuite/commit/9cd0054437c07b979349ca7a5d540e895897c135))

Completes the tree family with single-select counterparts: cascader (sibling of multi_cascade_tree)
  and tree_picker (sibling of check_tree_picker). Both return str | None, carry label/help a11y via
  FieldLabel, disabled_items=, locale=, and two-way value sync.

- cascader: column-by-column navigation, parent_selectable= to allow non-leaf answers, searchable,
  column_width/height. - tree_picker: searchable dropdown tree with virtualized=,
  default_expand_all, show_indent_line, only_leaf_selectable, height. - Registry entries in the
  shared bundle; shared chunk 637 -> 662 KB for both widgets together. - New e2e
  (test_cascader_tree_e2e.py): cascade column navigation round-trips a leaf value, tree leaf click
  round-trips, and a branch click under only_leaf_selectable does not change the selection. ccv2 e2e
  and smoke suites extended to 17 widgets. - Showcase app: new Trees > Cascader and TreePicker page
  with leaf-only vs parent-selectable cascaders, expanded and leaf-only trees, and usage code
  snippets. - README: tree table rows + API sections for both widgets.


## v0.8.0 (2026-07-11)

### Chores

- Bump demo app requirement to v0.7.1
  ([`71389fe`](https://github.com/lperezmo/st-rsuite/commit/71389fef7802d76c13e5112644023876e91f864c))

### Features

- Select_picker and tag_picker
  ([`52a053e`](https://github.com/lperezmo/st-rsuite/commit/52a053ebd050f17db7af64ca9f3bedf4f19f87ae))

Two new widgets wrapping RSuite SelectPicker and TagPicker: searchable single select and tag-style
  multi select, both with automatic grouping (items carrying a group key), virtualized= for very
  large lists, disabled_items=, label/help a11y via FieldLabel, and two-way value sync from day one.

- tag_picker supports creatable=: values the user types that are not in items become options and
  come back in the return list. - Registry entries in the shared bundle; shared chunk grew 611 ->
  637 KB for both widgets together. - New e2e (test_select_tag_e2e.py): click-to-select roundtrip,
  group headings render, disabled item is not selectable, created tag round-trips. ccv2 e2e and
  smoke suites extended to 15 widgets. - Showcase app: new Select and Tag pickers page with
  side-by-side comparisons against the st.selectbox / st.multiselect builtins, a virtualized
  2,000-item list, and usage code snippets. - README: component table rows + API sections for both
  widgets.


## v0.7.1 (2026-07-11)

### Chores

- Bump demo app requirement to v0.7.0
  ([`3497c5f`](https://github.com/lperezmo/st-rsuite/commit/3497c5f5ade5e2b484bf4c8d5660c097792f274d))

### Performance Improvements

- Single-bundle architecture
  ([`ffe50f7`](https://github.com/lperezmo/st-rsuite/commit/ffe50f720eb87c8b4932183121d34724f0d2fe67))

Register ONE CCv2 component (st-rsuite.rsuite) serving every widget from a single asset_dir; each
  widget module injects a kind discriminator into data via bind_kind and the bundle entry routes it
  to the matching React component. Public Python API unchanged.

- One Vite build: 12.52 MB of per-widget JS (13 copies of React, RSuite, and the injected
  stylesheet) collapses to 1.23 MB on disk; the wheel drops from 2.78 MB to 0.35 MB. - RSuite
  locales split into lazy chunks (chunk-<locale>-*.js) so a page downloads only the locale it
  renders; chunk names stay out of the js=index-*.js glob, which must match exactly one file. - A
  page mixing widgets fetches the entry bundle once instead of once per widget type; the new e2e
  asserts the single fetch and that the ja_JP chunk loads and localizes the calendar when served
  over the component asset route. - Size guard and wheel-contents checks updated for the new layout,
  including a guard against stale per-component files leaking in from a cached setuptools build/lib
  staging dir.


## v0.7.0 (2026-07-07)

### Chores

- Bump demo app requirement to v0.6.0
  ([`14bc436`](https://github.com/lperezmo/st-rsuite/commit/14bc436de3fdd6ad3f3a3013ceedf8ba5436902d))

### Features

- Associate labels with controls and add help tooltips
  ([`c437b65`](https://github.com/lperezmo/st-rsuite/commit/c437b656b7e72c2cce73b85b9448ed8b8dc9183d))

The six labeled date/time components rendered a bare <label> with no htmlFor, so screen readers did
  not connect it to the control and clicking the label did nothing. A shared FieldLabel now renders
  the label with htmlFor tied to the control's id (via React useId, forwarded to the RSuite input),
  which the e2e confirms by checking a label click focuses the input.

FieldLabel also adds an optional help tooltip, exposed as help= on all six components to match the
  st.* builtin convention: an info marker beside the label with the help text as its title.

Also documents that carousel item 'src' is read from the local filesystem and inlined, so it must be
  a trusted path, not unsanitized user input (a review finding).

Deferred (attempted, both need real work, both low priority): RTL layout (the CustomProvider rtl
  prop does not flip the portaled popups in the CCv2 no-shadow-DOM setup) and a high-contrast theme
  (no reliable host signal to auto-detect; wants an explicit opt-in). Both noted in the plan.

- test/test_a11y_e2e.py asserts every labeled component associates its label to a present control id
  and renders the help tooltip


## v0.6.0 (2026-07-07)

### Chores

- Bump demo app requirement to v0.5.0
  ([`db72940`](https://github.com/lperezmo/st-rsuite/commit/db72940bedd5720b0d507857d7d2a553108e56aa))

### Features

- Daterangepicker shortcut presets and calendar default month
  ([`4d625f0`](https://github.com/lperezmo/st-rsuite/commit/4d625f086254c5baa8aafe1c5bd213f148bca49e))

date_range_picker gains ranges= (custom shortcut presets beside the calendar) and
  default_calendar_value= (which month pair the panels open on). date_picker gains
  calendar_default_date=.

ranges follows RSuite's three-state contract: None keeps the built-in defaults (Today / Yesterday /
  Last 7 days), an explicit list replaces them, and an empty list removes the sidebar. Each preset
  is {"label", "value": (start, end)} with optional close_overlay and placement. A shared frontend
  helper (rangePresets.ts) converts the serialized ISO pairs into the [Date, Date] presets RSuite
  expects.

- test/test_range_shortcuts_e2e.py opens the overlay, asserts the custom presets render, clicks one,
  and checks the declared range round-trips to Python - README and the showcase gain a
  shortcut-ranges example


## v0.5.0 (2026-07-07)

### Chores

- Bump demo app requirement to v0.4.0
  ([`13940cd`](https://github.com/lperezmo/st-rsuite/commit/13940cdf4ee00a483837dbe2555266b3299f8ce3))

### Features

- Time constraints, editable, and loading
  ([`f8dde1e`](https://github.com/lperezmo/st-rsuite/commit/f8dde1e2c89683d4402a6780989180c7f46f43ba))

time_picker and time_range_picker gain min_hour, max_hour, hidden_hours, hidden_minutes, and
  hidden_seconds, mapped to RSuite's hideHours/hideMinutes/ hideSeconds via a shared frontend helper
  (timeConstraints.ts). This makes business-hours pickers (hide everything outside 09:00-17:00)
  possible, which they were not before.

Scope note: the standalone TimePicker/TimeRangePicker expose only the hide* family, not
  shouldDisableHour (that is DatePicker-in-time-mode only, verified against the RSuite v6 type
  defs), so hidden units are removed from the panel rather than shown-but-disabled.

All four popup pickers (date_picker, date_range_picker, time_picker, time_range_picker) also gain
  editable= (default True; False makes the field toggle-only) and loading= (default False)
  passthroughs. The keyboard-only date_input/date_range_input support neither in RSuite, so they are
  unchanged.

- test/test_time_constraints_e2e.py opens a 09:00-17:00 picker and asserts the hour column hides
  out-of-window hours while keeping in-window ones - README and the showcase gain a business-hours
  example


## v0.4.0 (2026-07-07)

### Chores

- Bump demo app requirement to v0.3.6
  ([`e637c51`](https://github.com/lperezmo/st-rsuite/commit/e637c51420a92fe8a3297a3d3623688d14846049))


## v0.3.6 (2026-07-07)

### Bug Fixes

- Sync Python value changes into mounted components
  ([`7ca48f5`](https://github.com/lperezmo/st-rsuite/commit/7ca48f5a998644e04f1a2c2bec5bea8f60aca6b8))

Every component seeded local React state once with useState(initialValue) and never reconciled, so
  any later change to the Python-side value= was silently ignored (reset buttons, dependent widgets,
  and Session-State-driven updates all failed). This is the initial-only-hydration pitfall the
  repo's own CCv2 state-sync reference warns about.

- add shared useSyncedValue hook: it remembers the last incoming value key and adopts a new value
  only when that key changes, so Python-driven changes propagate while user edits are preserved.
  Tracking the incoming key (not the user's emission) is what stops a static value= from reverting
  an edit on the next rerun, and makes the controlled-pattern echo a no-op that never fights an
  in-progress edit. - convert all 12 stateful components to the hook (timeline is display-only) -
  add test/test_value_sync_e2e.py: drives value= at runtime via a button and asserts the date_picker
  and check_tree adopt it, plus that a user edit still round-trips and is not reverted by the echo

Also fixes the 4 pre-existing frontend type errors this surfaced and adds a typecheck CI gate so
  they cannot recur: - CheckTree/CheckTreePicker onChange now types the RSuite ValueType
  ((string|number)[]) and coerces to string[] - DateRangeInput uses RSuite's nullable-element tuple
  value type - CheckTree and MultiCascadeTree have no RSuite disabled prop (it was a silent no-op);
  disabled is now honored via a wrapper that blocks interaction and dims the control, so the Python
  disabled= actually works - new typecheck job in tests.yml runs tsc --noEmit (the Vite build
  transpiles without type-checking, so nothing caught these before)

### Chores

- Bump demo app requirement to v0.3.5
  ([`6f1c5b1`](https://github.com/lperezmo/st-rsuite/commit/6f1c5b1e178e56db18613deb261864966ecc0a87))

### Features

- Declarative date constraints for the calendar pickers
  ([`f9f9a52`](https://github.com/lperezmo/st-rsuite/commit/f9f9a52ca1d67dc5119b4e3e5e7d18aafdb8ce7f))

date_picker and date_range_picker gain min_date, max_date, disabled_dates, disabled_weekdays,
  limit_start_year, and limit_end_year. Even st.date_input has min/max; the pickers had no way to
  restrict selectable dates at all.

Callables cannot cross the Python/JS boundary, so the wrappers send plain serialized values and a
  shared frontend helper (dateConstraints.ts) builds the RSuite shouldDisableDate predicate.
  disabled_weekdays uses Python's Monday-0 numbering (converted from JS Sunday-0 in the predicate).
  The keyboard-only date_input / date_range_input are intentionally excluded: RSuite has no calendar
  there to disable.

Also serialize a passed datetime as its .date() (a datetime previously produced a full timestamp
  that the frontend date parser could not read), which resolves the dead branch in
  date_picker._serialize.

- test/test_date_constraints_e2e.py opens the calendar and asserts min/max, disabled_dates, and
  disabled_weekdays render non-selectable cells while an in-range weekday stays selectable - README
  and the showcase gain a constraints example


## v0.3.5 (2026-07-07)

### Bug Fixes

- Ship minified production frontend builds without sourcemaps
  ([`9daff1e`](https://github.com/lperezmo/st-rsuite/commit/9daff1eb70b7984d2c8c69c0bf97ee5a960bee68))

Every published wheel so far contained unminified dev bundles plus sourcemaps because build.mjs
  keyed on NODE_ENV=production and no workflow ever set it (v0.3.4 wheel: 9.2 MB, 19.5 MB of
  unminified JS and 30.3 MB of maps unpacked).

- build.mjs now defaults to production; dev builds are opt-in through the existing build:dev / dev
  scripts that set NODE_ENV=development - switch production minify from esbuild to terser: Vite
  disables esbuild whitespace minification for lib-mode ES output, which left bundles at 1.3 MB+
  even with minify enabled - exclude *.js.map from the sdist (MANIFEST.in) and the wheel
  (exclude-package-data) as a guard - add scripts/assert_prod_build.sh and run it after every
  frontend build in tests.yml, release.yml, and publish.yml so a dev build can never ship again

Result: wheel drops from 9.2 MB to 2.8 MB, largest bundle from 1.66 MB to 1.07 MB (187 KB gzipped
  over the wire), no sourcemaps shipped.

### Chores

- Bump demo app requirement to v0.3.4
  ([`e9f748b`](https://github.com/lperezmo/st-rsuite/commit/e9f748bd84522864d7f5825e32651aebff413987))


## v0.3.4 (2026-06-23)

### Bug Fixes

- Support Streamlit 1.51 and 1.52 via an isolate_styles compat shim
  ([`bacd632`](https://github.com/lperezmo/st-rsuite/commit/bacd6323290eb881e321d7ddc8f6f55ecc4ff4b6))

Register all 13 components through st_rsuite/_compat.py, which applies isolate_styles=False at
  registration (Streamlit >=1.53) or on the per-call renderer (1.51/1.52). Lower the floor to
  streamlit>=1.51 and extend the smoke and e2e CI matrices to cover 1.51 and 1.52.

### Chores

- Bump artifact actions to v7 for the Node 24 runtime
  ([#2](https://github.com/lperezmo/st-rsuite/pull/2),
  [`453ca76`](https://github.com/lperezmo/st-rsuite/commit/453ca76f2156573a4c0063076252d94d6b4b04c8))

actions/upload-artifact@v5 and actions/download-artifact@v5 run on Node.js 20, which GitHub Actions
  has deprecated, so every Tests run logged a Node 20 warning.

Pin both to @v7, which declares runs.using: node24 (verified in each action.yml). The two actions
  reached their Node 24 default at different majors (upload-artifact in v6, download-artifact in
  v7), so v7 is the safe floor for both. No behavior change, only the runtime.

- Bump demo app requirement to v0.3.3
  ([`6943ed7`](https://github.com/lperezmo/st-rsuite/commit/6943ed71f9605e6f5ce7f7fd352dd11d96af62b1))


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
