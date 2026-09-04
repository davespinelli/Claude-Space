#!/usr/bin/env bash
# Download the latest filings bundle and unpack it into research/deepvalue/filings/.
#
# For cloud agents whose only reachable hosts are github.com, api.github.com and
# PyPI. GitHub Actions builds the bundle nightly (.github/workflows/filings.yml)
# and publishes it as the single asset on the rolling `filings-latest` release,
# so this needs no API token and no SEC access.
#
# Usage:
#   bash research/deepvalue/fetch_bundle.sh            # extract into place
#   bash research/deepvalue/fetch_bundle.sh --keep     # also keep the tarball
#   REPO=owner/name bash research/deepvalue/fetch_bundle.sh
#   BUNDLE_URL=file:///path/to/filings_bundle.tar.gz bash research/deepvalue/fetch_bundle.sh
set -euo pipefail

REPO="${REPO:-davespinelli/Claude-Space}"
TAG="${TAG:-filings-latest}"
ASSET="filings_bundle.tar.gz"
# BUNDLE_URL overrides the release URL (used by tests and for a manual mirror).
URL="${BUNDLE_URL:-https://github.com/${REPO}/releases/download/${TAG}/${ASSET}}"

# repo root = two levels up from this script (research/deepvalue/ -> repo root)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
DEST="${REPO_ROOT}/research/deepvalue/filings"

KEEP=0
[ "${1:-}" = "--keep" ] && KEEP=1

TMP="$(mktemp -d)"
cleanup() { [ "$KEEP" -eq 1 ] || rm -rf "$TMP"; }
trap cleanup EXIT

echo "Downloading ${URL}"
HTTP_CODE="$(curl -sS -L -w '%{http_code}' -o "${TMP}/${ASSET}" "${URL}" || echo 000)"

# Success is decided by the payload, not the status line: curl reports 000 for
# file:// URLs, and a captive proxy can return 200 with an HTML error page.
OK=0
if [ -s "${TMP}/${ASSET}" ] && tar -tzf "${TMP}/${ASSET}" >/dev/null 2>&1; then
  OK=1
fi

if [ "$OK" -ne 1 ]; then
  SIZE_TMP=$(wc -c < "${TMP}/${ASSET}" 2>/dev/null | tr -d ' ' || echo 0)
  echo ""
  echo "ERROR: could not download the filings bundle (HTTP ${HTTP_CODE})." >&2
  case "$HTTP_CODE" in
    404)
      cat >&2 <<EOF

The release '${TAG}' does not exist yet in ${REPO}, or it has no
'${ASSET}' asset attached.

The bundle is produced by the 'deep-value-filings' GitHub Actions workflow.
Someone with repo access needs to run it once:

  gh workflow run filings.yml --repo ${REPO}

or trigger it from the Actions tab (workflow_dispatch). It also runs nightly at
03:30 UTC. Check whether it has ever succeeded:

  gh run list --workflow filings.yml --repo ${REPO}
  gh release view ${TAG} --repo ${REPO}

If the repository is private, this script cannot fetch the asset anonymously;
export a token and retry:

  GH_TOKEN=... gh release download ${TAG} --repo ${REPO} --pattern '${ASSET}'
EOF
      ;;
    000)
      echo "" >&2
      echo "No network route to github.com. This environment cannot reach the" >&2
      echo "release host at all; check the egress allowlist." >&2
      ;;
    *)
      echo "" >&2
      echo "Downloaded ${SIZE_TMP:-0} bytes but it is not a valid gzip tar archive." >&2
      echo "It is probably an HTML error page. First bytes:" >&2
      head -c 200 "${TMP}/${ASSET}" 2>/dev/null >&2 || true
      echo "" >&2
      echo "Retry, or download by hand: ${URL}" >&2
      ;;
  esac
  exit 1
fi

SIZE=$(wc -c < "${TMP}/${ASSET}" | tr -d ' ')
echo "Downloaded ${SIZE} bytes"

mkdir -p "${DEST}"
# archive paths are rooted at research/deepvalue/filings/, so extract from the repo root
echo "Extracting into ${DEST}"
tar -xzf "${TMP}/${ASSET}" -C "${REPO_ROOT}"

N_TICKERS=$(find "${DEST}" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')
N_FILES=$(find "${DEST}" -type f | wc -l | tr -d ' ')

if [ "$N_FILES" -eq 0 ]; then
  echo "" >&2
  echo "ERROR: the archive extracted but ${DEST} is still empty." >&2
  echo "The bundle's internal paths are not rooted at research/deepvalue/filings/." >&2
  echo "Top-level entries in the archive:" >&2
  tar -tzf "${TMP}/${ASSET}" | cut -d/ -f1-3 | sort -u | head -5 >&2
  echo "Rebuild it with: python research/deepvalue/bundle.py" >&2
  exit 1
fi

echo "OK: ${N_FILES} files across ${N_TICKERS} ticker directories in ${DEST}"

if [ -f "${DEST}/MANIFEST.json" ]; then
  python3 - "${DEST}/MANIFEST.json" <<'PY' 2>/dev/null || true
import json, sys
m = json.load(open(sys.argv[1]))
t = m.get("tickers", {})
ok = sum(1 for r in t.values() if r.get("ok"))
print(f"manifest: {len(t)} tickers ({ok} ok), built {m.get('updated_at')}")
PY
fi

if [ "$KEEP" -eq 1 ]; then
  cp "${TMP}/${ASSET}" "${REPO_ROOT}/${ASSET}"
  echo "Kept tarball at ${REPO_ROOT}/${ASSET}"
fi
