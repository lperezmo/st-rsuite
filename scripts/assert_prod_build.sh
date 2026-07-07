#!/usr/bin/env bash
# Guard against accidentally shipping development frontend builds.
#
# A production (terser-minified) build of any st-rsuite component is currently
# 0.93-1.07 MB (roughly half of that is the injected rsuite stylesheet), while
# a dev build (NODE_ENV=development) is 1.33 MB+ unminified and writes .js.map
# files next to the bundles. The 1.2 MB limit sits between the two so a dev
# build can never ship. Run this after `npm run build` in any workflow that
# packages or tests the built assets.
set -euo pipefail

LIMIT_BYTES=1228800 # 1.2 MB
fail=0
found_js=0

for f in st_rsuite/*/frontend/build/*.js; do
  [ -e "$f" ] || continue
  found_js=1
  size=$(wc -c <"$f")
  if [ "$size" -gt "$LIMIT_BYTES" ]; then
    echo "FAIL: $f is $size bytes (limit $LIMIT_BYTES); looks like a dev build" >&2
    fail=1
  fi
done

if [ "$found_js" -eq 0 ]; then
  echo "FAIL: no built bundles found under st_rsuite/*/frontend/build/" >&2
  fail=1
fi

for f in st_rsuite/*/frontend/build/*.js.map; do
  [ -e "$f" ] || continue
  echo "FAIL: sourcemap $f present; production builds must not emit sourcemaps" >&2
  fail=1
done

if [ "$fail" -eq 0 ]; then
  echo "OK: all bundles minified (<=$LIMIT_BYTES bytes) and no sourcemaps present"
fi
exit "$fail"
