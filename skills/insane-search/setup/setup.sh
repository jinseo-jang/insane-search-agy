#!/usr/bin/env bash
# First-run setup for insane-search. Idempotent, non-blocking.
# Compatible with Antigravity CLI, IDE, AGY 2.0, and standard AI agents.

set -uo pipefail

PLUGIN="insane-search"
OWN_REPO="fivetaku/insane-search"
HUB_REPO="fivetaku/gptaku_plugins"

CONFIG_DIR="${GEMINI_CONFIG_DIR:-${ANTIGRAVITY_CONFIG_DIR:-$HOME/.gemini}}"
HERE="$(cd "$(dirname "$0")" && pwd)"
MARKER_DIR="$HOME/.gptaku-setup"
SETUP_MARKER="$MARKER_DIR/$PLUGIN.json"
STAR_MARKER="$MARKER_DIR/$PLUGIN.star.json"
mkdir -p "$MARKER_DIR"

# --- record the star decision (and star the repos on "yes") ---
write_star() {  # $1 = decision (yes|no|asked)
  ts=$(date +%s 2>/dev/null || echo 0)
  printf '{"star_decision":"%s","plugin":"%s","ts":%s}\n' "$1" "$PLUGIN" "$ts" > "$STAR_MARKER"
}

if [ "${1:-}" = "star" ]; then
  DECISION="${2:-no}"
  write_star "$DECISION"
  if [ "$DECISION" = "yes" ] && command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
    for repo in "$OWN_REPO" "$HUB_REPO"; do
      gh api "user/starred/$repo" >/dev/null 2>&1 || gh api -X PUT "user/starred/$repo" >/dev/null 2>&1 || true
    done
  fi
  exit 0
fi

# --- first-run env checks (silent, once per machine) ---
if [ ! -f "$SETUP_MARKER" ]; then
  ts=$(date +%s 2>/dev/null || echo 0)
  printf '{"setup":true,"plugin":"%s","ts":%s}\n' "$PLUGIN" "$ts" > "$SETUP_MARKER"
fi

# --- ask mode: emit the star prompt EXACTLY ONCE ---
if [ "${1:-}" = "ask" ] && [ ! -f "$STAR_MARKER" ]; then
  write_star "asked"
  echo "STAR_ASK ko"
fi
exit 0
