#!/bin/sh
# Installs the no-merge-to-main guards into this clone's .git/hooks (hooks are not versioned,
# so every clone runs this once). Copies, rather than links, so they stay in place when main,
# which lacks tools/git-hooks/, is checked out. An existing hook of the same name is kept as <name>.bak.
set -e
src=$(cd "$(dirname "$0")" && pwd)
hooks=$(git rev-parse --git-path hooks)
mkdir -p "$hooks"
for name in pre-merge-commit pre-push post-merge; do
  if [ -f "$hooks/$name" ] && ! cmp -s "$src/$name" "$hooks/$name"; then
    mv "$hooks/$name" "$hooks/$name.bak"
  fi
  cp "$src/$name" "$hooks/$name"
  chmod +x "$hooks/$name"
  echo "installed $hooks/$name"
done
