#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="${XDG_BIN_HOME:-$HOME/.local/bin}"
DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
APPS_DIR="$DATA_HOME/applications"
ICON_DIR="$DATA_HOME/icons/hicolor/scalable/apps"
DESKTOP_TEMPLATE="$ROOT_DIR/packaging/linux/foundry-app.desktop.in"
DESKTOP_TARGET="$APPS_DIR/foundry-app.desktop"
ICON_SOURCE="$ROOT_DIR/packaging/linux/foundry-app.svg"
ICON_TARGET="$ICON_DIR/foundry-app.svg"
BIN_TARGET="$BIN_DIR/foundry-app"

mkdir -p "$BIN_DIR" "$APPS_DIR" "$ICON_DIR"

ln -sfn "$ROOT_DIR/foundry-app" "$BIN_TARGET"
install -m 644 "$ICON_SOURCE" "$ICON_TARGET"
sed \
  -e "s|__ROOT__|$ROOT_DIR|g" \
  -e "s|__BIN__|$BIN_DIR|g" \
  "$DESKTOP_TEMPLATE" >"$DESKTOP_TARGET"
chmod 644 "$DESKTOP_TARGET"

if command -v update-desktop-database >/dev/null 2>&1; then
  update-desktop-database "$APPS_DIR" >/dev/null 2>&1 || true
fi

cat <<EOF
Foundry is installed.

What this did:
- linked foundry-app into $BIN_DIR
- installed a Foundry desktop entry into $APPS_DIR
- installed the Foundry icon into $ICON_DIR

Commands:
  foundry-app            open Foundry
  foundry-app --status   show app status
  foundry-app --stop     stop the browser app
  foundry-app --cleanup  remove stale launcher state

No systemd service was created.
Foundry starts only when you open it.
Use the Foundry Shutdown button or: foundry-app --stop

If your shell does not already include $BIN_DIR, add this:
  export PATH="$BIN_DIR:\$PATH"
EOF
