#!/bin/sh
set -eu
base=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
target="${XDG_DATA_HOME:-$HOME/.local/share}/framedrop"
mkdir -p "$target" "${XDG_DATA_HOME:-$HOME/.local/share}/applications"
cp -R "$base/FrameDrop/." "$target/"
chmod +x "$target/FrameDrop"
cat > "${XDG_DATA_HOME:-$HOME/.local/share}/applications/framedrop.desktop" <<ENTRY
[Desktop Entry]
Type=Application
Name=FrameDrop
Comment=Save public videos locally
Exec="$target/FrameDrop"
Terminal=false
Categories=AudioVideo;
ENTRY
printf 'FrameDrop installed. Open it from your application menu.\n'
