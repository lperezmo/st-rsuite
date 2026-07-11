#!/usr/bin/env bash
# Guard against accidentally shipping development frontend builds.
#
# The production (terser-minified) single-bundle build is an index-*.js entry
# (~0.45 MB), a shared chunk-index-*.js (~0.6 MB, includes the injected rsuite
# stylesheet), and per-locale chunks under 15 KB. A dev build (NODE_ENV=
# development) leaves the shared chunk unminified at ~1.9 MB and writes .js.map
# files next to the bundles. The 1.2 MB per-file limit sits between the two so
# a dev build can never ship. Run this after `npm run build` in any workflow
# that packages or tests the built assets.
set -euo pipefail

LIMIT_BYTES=1228800 # 1.2 MB
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
