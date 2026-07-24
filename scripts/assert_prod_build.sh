#!/usr/bin/env bash
# Guard against accidentally shipping development frontend builds.
#
# Since the vite 8 / Rolldown bump the production (terser-minified) build is a
# single index-*.js entry (~1.11 MB, including the injected rsuite stylesheet;
# there is no separate shared chunk-index-*.js any more) plus per-locale chunks
# under 20 KB. A dev build (NODE_ENV=development) leaves that entry unminified
# at ~2.56 MB and writes .js.map files next to the bundles.
#
# The 1.6 MB per-file limit sits between the two: ~44% of headroom above the
# current production entry, so ordinary dependency growth does not trip it,
# while still well under the dev-build size. The sourcemap check below catches
# dev builds independently, so this is a size sanity check rather than the only
# line of defense. Run this after `npm run build` in any workflow that packages
# or tests the built assets.
set -euo pipefail

LIMIT_BYTES=1677721 # 1.6 MB
fail=0
found_entry=0

for f in st_rsuite/frontend/build/*.js; do
  [ -e "$f" ] || continue
  case "$(basename "$f")" in index-*.js) found_entry=$((found_entry + 1)) ;; esac
  size=$(wc -c <"$f")
  if [ "$size" -gt "$LIMIT_BYTES" ]; then
    echo "FAIL: $f is $size bytes (limit $LIMIT_BYTES); looks like a dev build" >&2
    fail=1
  fi
done

if [ "$found_entry" -ne 1 ]; then
  echo "FAIL: expected exactly one index-*.js entry under st_rsuite/frontend/build/, found $found_entry (the Python side registers js=\"index-*.js\", which must match exactly one file)" >&2
  fail=1
fi

for f in st_rsuite/frontend/build/*.js.map; do
  [ -e "$f" ] || continue
  echo "FAIL: sourcemap $f present; production builds must not emit sourcemaps" >&2
  fail=1
done

if [ "$fail" -eq 0 ]; then
  echo "OK: all bundles minified (<=$LIMIT_BYTES bytes), exactly one entry, no sourcemaps"
fi
exit "$fail"
