#!/usr/bin/env bash
# Regenerate the static library index.html from server.js (source of truth).
# Starts the Express app on an ephemeral port, snapshots "/", fixes the
# canonical URL, and writes index.html at the repo root.
set -euo pipefail
cd "$(dirname "$0")/.."

PORT=3977
rm -f index.html   # otherwise express.static shadows the dynamic route
PORT=$PORT node server.js &
SRV=$!
trap 'kill $SRV 2>/dev/null || true' EXIT
for i in $(seq 1 30); do
  curl -sf "http://localhost:$PORT/" -o /tmp/sb-index.$$ && break
  sleep 0.5
done
[ -s /tmp/sb-index.$$ ] || { echo "index snapshot failed"; exit 1; }
sed 's|<link rel="canonical" href="https://spanish-books.onrender.com/">|<link rel="canonical" href="https://www.beibeiamigos.com/spanish-books/">|' /tmp/sb-index.$$ > index.html
rm -f /tmp/sb-index.$$
echo "index.html rebuilt: $(grep -o '[0-9]* libros disponibles' index.html)"
