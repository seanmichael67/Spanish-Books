#!/usr/bin/env bash
# Rebuild the static library page from server.js without publishing it.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORT="${PORT:-3456}"
TMP="$(mktemp "${TMPDIR:-/tmp}/spanish-books-index.XXXXXX.html")"
LOG="$(mktemp "${TMPDIR:-/tmp}/spanish-books-server.XXXXXX.log")"
PID=""

cleanup() {
  [[ -n "$PID" ]] && kill "$PID" 2>/dev/null || true
  rm -f "$TMP" "$LOG"
}
trap cleanup EXIT

PORT="$PORT" node "$ROOT/server.js" >"$LOG" 2>&1 &
PID=$!

for _ in $(seq 1 50); do
  if curl --fail --silent --show-error "http://127.0.0.1:${PORT}/" -o "$TMP"; then
    break
  fi
  if ! kill -0 "$PID" 2>/dev/null; then
    printf 'server.js exited before rendering the library:\n' >&2
    cat "$LOG" >&2
    exit 1
  fi
  sleep 0.1
done

if [[ ! -s "$TMP" ]]; then
  printf 'Failed to render the library page.\n' >&2
  cat "$LOG" >&2
  exit 1
fi

for marker in 'id="bookSearch"' 'id="resultsStatus"' 'https://www.beibeiamigos.com/spanish-books/'; do
  if ! python3 - "$TMP" "$marker" <<'PY'
from pathlib import Path
import sys
raise SystemExit(0 if sys.argv[2] in Path(sys.argv[1]).read_text(encoding="utf-8") else 1)
PY
  then
    printf 'Generated index is missing required marker: %s\n' "$marker" >&2
    exit 1
  fi
done

mv "$TMP" "$ROOT/index.html"
printf 'Rebuilt %s from server.js (local only).\n' "$ROOT/index.html"
