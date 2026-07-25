# CHANGELOG


## v0.9.1 (2026-07-25)

### Bug Fixes

- Disable trees with a fieldset so they stay readable
  ([`42b0862`](https://github.com/lperezmo/st-rsuite/commit/42b08623565083943072ec0f68ce14d0f844ade5))

inert on the wrapper kept the keyboard out by removing the subtree from the accessibility tree as
  well, so a screen reader announced nothing at all where sighted users saw a dimmed tree with
  checked boxes, and the wrapper's own aria-disabled went unread with it.

A disabled <fieldset> disables every form control inside it natively: the checkboxes and the search
  box leave the tab order and are announced as unavailable, while the tree itself stays readable.

Not RSuite's own disabledItemValues, the obvious alternative: it renders a disabled node as
  unchecked whatever value says, so a disabled tree would show none of the selection it exists to
  display. Measured in the browser, React went from aria-checked=true to false under it.

The e2e guards are new: one that nothing is inert and every control is :disabled, one that the
  checked node still reads as checked. Both fail against the inert build; the second also fails
  against disabledItemValues.

- Range on_change firing, theme re-detection, datetime defaults, disabled trees
  ([`c5ce0a6`](https://github.com/lperezmo/st-rsuite/commit/c5ce0a692204b034895310448483353ed85f90d8))

CCv2 dispatches change callbacks per state key, not per widget: Streamlit diffs the widget state
  dict and runs metadata.callbacks[key] for each changed key. The range widgets registered the user
  callback on the start key only and a no-op on the end key, so extending, shortening, or moving
  only the end of a range silently skipped on_change. Both keys now share one callback wrapped in
  _callbacks.single_fire, whose per-render closure flag keeps a both-ends change from firing it
  twice.

Theme detection cached forever and never re-detected. The cache key came from --st-background-color
  read off document.documentElement, but Streamlit spreads those custom properties onto a
  per-component wrapper div and custom properties only inherit downward, so the value was always
  empty and the first result was pinned for the life of the page, shared by every widget in the
  bundle. Flipping Streamlit appearance left calendars and popups on the stale theme. The theme is
  now resolved per render from the component's own element.

date_input and date_range_input serialized a datetime default as a full timestamp because they
  tested isinstance(d, date) first and datetime is a subclass of date. The frontend then parsed an
  Invalid Date and the Python side raised in date.fromisoformat and swallowed it, so the default
  vanished on both sides. Hoisted the correct ordering into _dates.serialize_date and reused it
  across all four date widgets.

Other fixes:

- check_tree / multi_cascade_tree disabled=True was mouse-only. pointerEvents blocks the pointer but
  RSuite tree items stay in the tab order, so a keyboard user could Tab in and toggle checkboxes
  back to Python. Added inert on the wrapper, with a React 18 JSX type declaration for the
  attribute. - pin_input flipped controlled to uncontrolled once the user cleared every digit,
  because the value prop fell back to undefined and handed control back to RSuite internal state. -
  radio_tile coerced a selected empty-string option to None, so an option whose value is the empty
  string was indistinguishable from no selection. - keyOfList joined on a literal NUL byte, which
  made the whole file read as binary to git and to text tooling. Same separator, written as an
  escape.

### Chores

- Add regression tests for the reviewed fixes
  ([`ff258f2`](https://github.com/lperezmo/st-rsuite/commit/ff258f21e972905758b7b9f6def5193e4567fc4b))

The 13 reviewed defects shipped with no test that would catch a regression: the suite sat at 55 on
  both main and this branch. Add 48 tests covering the behavioral fixes, each verified to fail
  against the unfixed code.

Python units (no browser):

- test_date_serialization.py pins serialize_date's datetime-before-date check. A datetime default
  used to serialize to a full timestamp, which the frontend rendered as an Invalid Date and
  date.fromisoformat rejected on the way back, so the default vanished on both sides. -
  test_range_callbacks.py captures the callbacks each range widget registers and drives them through
  Streamlit's own per-key dispatcher (SessionState._dispatch_json_change_callbacks), so the
  production dispatch path is under test rather than a stand-in. Covers the reported bug (only the
  end of a range changing skipped on_change entirely), the dedupe when both ends move, and the
  no-change case. - test_radio_tile_return.py pins the empty string as a real option value, distinct
  from no selection at all.

Browser (test_review_findings_e2e.py + review_findings_e2e_app.py):

- datetime defaults reach date_input and date_range_input as dates, - a disabled check_tree /
  multi_cascade_tree refuses focus and stays out of the tab order, so a keyboard user can no longer
  toggle a "disabled" tree, - ["New York"] and ["New", "York"] stay distinct value-sync keys,
  locking in the NUL join in keyOfList, - the RSuite theme re-detects when Streamlit's appearance
  flips, instead of serving a cache pinned at first render.

No test for the PinInput controlled/uncontrolled fix: with RSuite's useControlled, value={pinValue
  || undefined} and value={pinValue} are observationally identical from the browser, and the React
  warning that would distinguish them is stripped from the production bundle. Tests written against
  it passed on the unfixed code, so they were dropped rather than kept as false coverage.

- Adopt ruff 0.16 and lint in CI, matching st-aggrid
  ([`564d576`](https://github.com/lperezmo/st-rsuite/commit/564d576c3de2c844e967c5e0f814d466ebf11c0a))

This repo carried a [tool.ruff] section with an extend-exclude and nothing that ever read it: no
  ruff in the dev group, no lint job in tests.yml. So the Python side had no linting at all while
  the frontend had a typecheck gate.

Pinned to ruff>=0.16,<0.17 with the same reasoning as the sibling st-aggrid repo. The upper bound is
  the load-bearing half: ruff-action installs the newest release satisfying the constraint, and
  0.16.0 grew the default rule set from 59 rules to 413, which turned st-aggrid's CI red on 143
  findings in untouched code. An unbounded floor would hand this repo the same surprise on the next
  expansion.

76 findings, 59 of them fixed automatically: deprecated typing imports rewritten to builtins and PEP
  604 unions (the floor is 3.10, so both are available), plus import sorting. A further 20 came from
  configuring known-local-folder and were also mechanical: examples import `utils` and tests import
  `e2e_utils` by path rather than as installed packages, so without that setting they sorted above
  st_rsuite itself and read as if the demos were importing the library from somewhere else.

One real fix rather than a suppression: e2e_utils logged through logging.getLogger(__file__), so the
  logger was named after an absolute path instead of the module.

The rest are suppressed per file with the reason recorded, never project-wide. DTZ wants explicit
  tzinfo everywhere, and every one of its 23 findings is in a date picker demo or a date test, none
  in the shipped package. A naive date.today() is what a date picker demo should show, and
  test_date_serialization holds naive and tz-aware values side by side with a test named
  test_naive_datetime_drops_the_time, so requiring tzinfo would mean deleting the cases that cover
  the behavior. SIM115 and PYI034 are scoped to test/e2e_utils.py: the temp file is deliberately
  owned across start() and stop(), and typing.Self is 3.11+ while this package supports 3.10 without
  typing_extensions.

The lint job runs `check .` rather than a directory list. A list stops covering whatever is added
  later, which is exactly how new test files went unrun in st-aggrid until markers replaced the
  filenames in its workflow.

45 non-browser tests pass, every changed file compiles, and every import in them resolves. The 20
  example pages have no test coverage, so they were checked that way rather than assumed.

- Bump demo app requirement to v0.9.0
  ([`91a8ad2`](https://github.com/lperezmo/st-rsuite/commit/91a8ad2d631c211483ee69e45775a2295440bcb9))

- Drop the stale July 7 review report
  ([`ebf1bb9`](https://github.com/lperezmo/st-rsuite/commit/ebf1bb9887607ce8e6c99fd62e13cc0d4ed2cb3c))

A 1200-line static report added by this branch, titled for v0.3.4 and listing three findings
  (unminified dev wheels, Python-side value changes never reaching the widget, React and RSuite
  bundled 13 times) that were all resolved across 0.4 to 0.7. The repo is at 0.9.0. Checked in under
  docs/ with no index or date context, it reads as a list of currently open defects, and it has
  nothing to do with the fixes on this branch. It stays in the history of the commit that added it.

- Fix stale prod-build guard, bump postcss, correct build.mjs comment
  ([`cbca040`](https://github.com/lperezmo/st-rsuite/commit/cbca0401c1c323de874b77f65ee0977c05b56398))

assert_prod_build.sh still described the pre-vite-8 output shape: an index-*.js entry of about 0.45
  MB plus a shared chunk-index-*.js of about 0.6 MB. Rolldown consolidated that shared chunk into
  the entry, which is now 1,113,228 bytes, or 90.6 percent of the 1.2 MB per-file limit. The next
  non-trivial dependency would have failed publish.yml and release.yml with a dev-build error on a
  perfectly good production bundle. Raised the limit to 1.6 MB, measured against a real dev build at
  2,558,072 bytes so the guard still separates the two, and rewrote the comment for the single-file
  output. The sourcemap check continues to catch dev builds independently.

npm audit reported 1 high (postcss GHSA-r28c-9q8g-f849, path traversal in previous-source-map
  auto-loading), contradicting the 0-vulnerabilities claim in 0065587. npm audit fix bumps the
  transitive postcss 8.5.17 to 8.5.23 and nanoid 3.3.15 to 3.3.16, both dev-only under vite. Build
  and typecheck still pass.

build.mjs justified terser in terms of esbuild skipping whitespace minification in lib mode, but
  esbuild left the tree with vite 8. Terser is still the right choice for drop_console /
  drop_debugger; the comment now says so.

- Pin 1.59 and 1.60 legs on the version matrix
  ([`f01b1a6`](https://github.com/lperezmo/st-rsuite/commit/f01b1a6d04d4a56a93ebe9b92e43b8cff477db42))

The Python job claims to run across every supported Streamlit minor, but it pinned 1.51 through 1.58
  and left the rest to the floating leg. That leg installs whatever is newest, so it covered 1.59
  and 1.60 only until 1.61 ships, at which point both would silently fall out of the matrix with the
  dependency still declared as streamlit>=1.51.

Verified locally before pinning: the full suite, browser tests included, passes on 1.59.2 and
  1.60.0.

e2e stays a subset on purpose. Its legs track the compat-shim boundaries (1.51 and 1.52 take
  isolate_styles at the call site, 1.53 at registration, 1.55 is the first that repaints on a live
  appearance change) plus the floating leg, and a pinned 1.60 there would only duplicate what latest
  already runs today.

- Prove the theme bridge follows an appearance change unaided
  ([`f7d03f6`](https://github.com/lperezmo/st-rsuite/commit/f7d03f67c815ef761863d0804af754f2b11fe73d))

A reviewer read the renderer and concluded the uncached theme read only helps a render that happens
  anyway, since Streamlit re-invokes a renderer for data and state changes: flip the appearance and
  touch nothing else, and every widget would sit on the old theme.

Measured instead of argued, with the theme read compiled out of the picture: on 1.51 (Settings
  dialog) and 1.55 (menu icons), changing the appearance and touching nothing else moved
  document.body from rs-theme-light to rs-theme-dark. Streamlit does re-invoke the renderer on an
  appearance change, so there is nothing to subscribe to and a watcher here would be dead weight.
  The docstring now records that.

The e2e test drops its rerender click, and the fixture drops the button behind it: driving a rerun
  first would hide a re-introduced cache behind the fresh render it would have got anyway. It also
  flips back to light, so following once on the way to a value it would have reached regardless is
  not enough to pass.

The skip comment claimed six versions; the e2e matrix has five legs and only two clear the >= 1.54
  floor. Corrected, with the note that the in-app appearance control does repaint on 1.51, so a
  menu-driven test would run everywhere at the cost of following Streamlit's menu markup.

- Refuse to release a tip the Tests run did not cover
  ([`f1af172`](https://github.com/lperezmo/st-rsuite/commit/f1af1726400c29515897d75886c6e1ae514bc523))

The release job is gated on a green Tests run but checked out ref: main, so it released whatever the
  tip was rather than the commit that passed. Push A goes green, push B lands a second later, and
  the workflow_run event for A checks out B, tags it and publishes it to PyPI while Tests-B is still
  running or already red. That is the race the gating was added to close.

The tip is still what gets checked out, because semantic-release has to commit and push back to the
  branch; a guard step now compares it to workflow_run.head_sha and skips the release when they
  differ. Skipped rather than failed: a second push is ordinary, it brings its own Tests and Release
  runs, and semantic-release reads every commit since the last tag, so the skipped release is folded
  into that later run rather than lost.

- Require a push event to reach the release job
  ([`acd9420`](https://github.com/lperezmo/st-rsuite/commit/acd9420f888d9d787c0d7578285551902ddfe54f))

The branches filter on a workflow_run trigger matches the triggering run's head branch, and Tests
  also runs on pull_request, so a fork PR opened from the contributor's own main branch satisfied it
  and could reach the PyPI publish. The old push trigger was unreachable from forks, so gating on
  Tests widened the surface. Requiring the upstream event to be a push closes it. Also documented
  why the checkout takes the tip of main rather than workflow_run.head_sha.

- Resolve all open Dependabot alerts via vite 8 and lockfile bumps
  ([`0065587`](https://github.com/lperezmo/st-rsuite/commit/0065587b1e685e60616a87d8bee4fe2fe67a34aa))

Frontend (st_rsuite/frontend): - vite 7.1.12 -> 8.1.4, @vitejs/plugin-react 5.1.0 -> 6.0.3. Vite 8
  bundles with Rolldown, so esbuild and @babel/core leave the dependency tree entirely. The build
  keeps minify: terser, which remains a supported opt-in path in vite 8; only the removed minify:
  esbuild path is gone, and this repo never used it.

- Transitive bumps in package-lock.json: lodash 4.18.1, postcss 8.5.17, picomatch 4.0.5. npm audit:
  0 vulnerabilities.

Python (uv.lock, all dev/example pins; runtime dep is streamlit only): - tornado 6.5.7, GitPython
  3.1.50, pillow 12.3.0, urllib3 2.7.0, idna 3.18, requests 2.34.2.

No source changes. Streamlit floor (>=1.51) and the _compat.py shim are untouched. Verified locally:
  npm ci + npm run build (hashed index-*.js entry and chunk-* naming intact), tsc --noEmit,
  scripts/assert_prod_build.sh, ruff check, 4 smoke + 51 Playwright e2e tests passing on Streamlit
  1.55.

- Restore the interpreter after stubbing the registration
  ([`b38b7c4`](https://github.com/lperezmo/st-rsuite/commit/b38b7c419e93bd7d38c692e11ddbb67c839c8ce5))

Both unit tests popped st_rsuite._component and the widget module out of sys.modules, re-imported
  them under a patched _compat.component, and left it that way. Two things then outlived the test:
  sys.modules kept the stub-bound module, so a later test asking for the real widget would get
  canned answers, and importing the submodule rebound it as an attribute of the package, shadowing
  the function st_rsuite.__getattr__ binds there. After that, from st_rsuite import radio_tile hands
  out a module and calling it raises TypeError: 'module' object is not callable.

That was survivable while each file was a CI job of its own. The matrix now runs pytest test/ in one
  process, where the next test to touch a widget collects the wreckage.

registration_stub owns the import and the cleanup, restoring both sys.modules and the package
  attribute, with a test that says so.

- Run the whole browser-less suite on the version matrix
  ([`e00c37b`](https://github.com/lperezmo/st-rsuite/commit/e00c37ba148d08491ca064965f5bfe2758d5efdd))

The matrix job was named "Smoke" and ran exactly one file, test/test_registration_smoke.py. That was
  accurate as a name and wrong as coverage: three browser-less files (date serialization, radio tile
  returns, range callbacks) never ran against any Streamlit version except the one the browser job
  happened to be on, because that job ran the whole directory.

So a pure-logic regression could only surface as a failure inside a Playwright leg, where it read as
  a browser flake, and only on the five versions e2e covers rather than the nine here. The sibling
  st-aggrid repo has had the wider coverage all along, and it is exactly where its pandas 3 NaT
  regression appeared: on a single leg of a matrix like this one.

Suites are now selected by the `browser` marker, matching st-aggrid. Enumerating filenames has
  already failed twice in this repo: it dropped five e2e files including the whole useSyncedValue
  regression guard, and it is what limited this job to one file. A marker makes inclusion the
  default, so a new test file joins the right job without anyone remembering to edit the workflow.

Python (Streamlit X) pytest test/ -m "not browser" 45 tests, 9 versions e2e (Streamlit X) pytest
  test/ -m browser 58 tests, 5 versions

45 + 58 = 103, the full collection, so nothing is unclassified and nothing runs twice.

The job is renamed from smoke to python-suite. "Smoke" now understates what it runs, and matching
  st-aggrid means the two repos read the same in a checks list. Neither main branch is protected, so
  no required-check name depends on the old one.

- Run the whole e2e suite in CI and gate PyPI publish on Tests
  ([`e69eb7b`](https://github.com/lperezmo/st-rsuite/commit/e69eb7b5a882dee1ec88c9db4abc2f4492590c79))

The e2e leg enumerated four test files by hand, so five never ran anywhere: test_value_sync_e2e (3
  tests), test_a11y_e2e (2), test_date_constraints_e2e (4), test_range_shortcuts_e2e (2),
  test_time_constraints_e2e (2). That is 13 of 26 e2e tests dead, including the entire
  useSyncedValue regression guard. The leg now runs pytest test/ so a new test file is covered the
  moment it lands.

release.yml triggered on push to main and ran python-semantic-release plus the PyPI publish with no
  dependency on tests.yml, which triggers independently on the same event. A merge whose typecheck
  or e2e legs were still running or already red could be tagged and shipped. release.yml now
  triggers on workflow_run of Tests and only proceeds when that run concluded successfully, with a
  non-cancelling concurrency group so two closely spaced merges cannot interleave their releases.

- Skip the appearance-flip test where Streamlit cannot flip
  ([`1c5ab07`](https://github.com/lperezmo/st-rsuite/commit/1c5ab0728a04bbac336e6cae27a250505edf05df))

The theme re-detection test failed on the 1.51, 1.52 and 1.53 legs of the e2e matrix and passed on
  1.54 through latest. The step that timed out was the wait for Streamlit's own
  --st-background-color to move after emulating prefers-color-scheme: dark, which runs before the
  component is involved at

all: those Streamlit versions do not repaint on a live appearance change, so there was no flip for
  the bridge to follow and the test was asserting against a precondition it could not establish.

Gate it on the capability instead. Reloading the page would make the test pass everywhere, but a
  reload remounts the component and re-detects the theme correctly even with the bug, so it would no
  longer catch the cache that pinned the appearance at first render. That is the whole point of the
  test, so the flip has to stay in-page.

The fix itself is version independent and is still exercised on six Streamlit versions. Parsed with
  packaging rather than splitting on dots so a prerelease like 1.54.0rc1 cannot crash the module at
  import.

- Upgrade gitpython to clear the pip advisories
  ([`3ee080d`](https://github.com/lperezmo/st-rsuite/commit/3ee080d214667f5363c8b7d303074046f458fec0))

Clears all four open Dependabot alerts on this repo: GHSA-v396-v7q4-x2qj, GHSA-2f96-g7mh-g2hx and
  GHSA-956x-8gvw-wg5v (patched in 3.1.51) plus GHSA-rwj8-pgh3-r573 (patched in 3.1.52). The resolver
  went to 3.1.55.

GitPython arrives only as a transitive dependency of streamlit, and uv.lock ships in neither the
  wheel nor the sdist, so the exposure is CI and contributors rather than anyone installing the
  package. Pillow was already at 12.3.0 here, which is why this repo has no Pillow alerts.

103 tests still pass.

### Documentation

- Drop em dashes and emoji, document help= on six components
  ([`1603a1e`](https://github.com/lperezmo/st-rsuite/commit/1603a1ec88b7eed8654caa9af7f5be7348c35656))

Removed all 19 em dashes from tracked files (project style rule): README, CHANGELOG, pyproject
  description (which ships as PyPI package metadata), .streamlit/config.toml, and the carousel /
  inputs / ui example modules. Swept every tracked file rather than a fixed list; the count is now
  zero. CHANGELOG is generated by semantic-release and will be rewritten on the next release, which
  is fine.

The quick-start block embedded two emoji as radio_tile icon values inside a python fence. That is
  code, so no emoji: the example now uses plain letters and a comment noting the field renders any
  short string.

The README signature blocks for date_picker, date_range_picker, time_picker, time_range_picker,
  date_input and date_range_input omitted help=, which all six accept and document in their
  docstrings, while select_picker, tag_picker, tree_picker and cascader listed it. Added it to the
  six for consistency.


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
