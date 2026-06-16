#!/usr/bin/env bash

set -euo pipefail

APP_NAME="pac-man"
VERSION="1.0.0"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_DIR="${ROOT_DIR}/dist"
BUILD_DIR="${ROOT_DIR}/build"
RELEASE_DIR="${ROOT_DIR}/release"
PACKAGE_DIR="${DIST_DIR}/${APP_NAME}"
ZIP_NAME="${APP_NAME}-linux-${VERSION}.zip"

cd "${ROOT_DIR}"

require_file() {
	if [ ! -f "$1" ]; then
		echo "Missing required file: $1" >&2
		exit 1
	fi
}

require_dir() {
	if [ ! -d "$1" ]; then
		echo "Missing required directory: $1" >&2
		exit 1
	fi
}

command -v python3 >/dev/null 2>&1 || {
	echo "Error: python3 is required." >&2
	exit 1
}

command -v uv >/dev/null 2>&1 || {
	echo "Error: uv is required." >&2
	exit 1
}

WHL="${WHL:-}"

if [ -z "${WHL}" ] && [ -f "${ROOT_DIR}/mazegenerator-2.0.2-py3-none-any.whl" ]; then
	WHL="${ROOT_DIR}/mazegenerator-2.0.2-py3-none-any.whl"
fi

if [ -z "${WHL}" ] && [ -f "${ROOT_DIR}/../mazegenerator-2.0.2-py3-none-any.whl" ]; then
	WHL="${ROOT_DIR}/../mazegenerator-2.0.2-py3-none-any.whl"
fi

UV_RUN=(uv run)

if [ -n "${WHL}" ]; then
	require_file "${WHL}"
	UV_RUN+=(--with "${WHL}")
	echo "Using extra wheel: ${WHL}"
fi

echo "Locating mazegenerator module..."
MAZEGENERATOR_FILE="$(
	"${UV_RUN[@]}" python - << 'PY'
from pathlib import Path
import inspect
import mazegenerator

print(Path(inspect.getfile(mazegenerator)).resolve())
PY
)"

require_file "${MAZEGENERATOR_FILE}"
echo "Using mazegenerator from: ${MAZEGENERATOR_FILE}"

echo "Checking required package files..."
require_file "${ROOT_DIR}/pac-man.py"
require_file "${ROOT_DIR}/default.json"
require_file "${ROOT_DIR}/highscores.json"
require_file "${ROOT_DIR}/README.md"
require_file "${ROOT_DIR}/fonts/PixelOperator-Bold.ttf"
require_file "${ROOT_DIR}/src/sprites/spritesheet.png"
require_dir "${ROOT_DIR}/docs"

echo "Cleaning previous package files..."
rm -rf "${DIST_DIR}" "${BUILD_DIR}" "${RELEASE_DIR}"
mkdir -p "${RELEASE_DIR}"

echo "Building executable with PyInstaller..."
"${UV_RUN[@]}" python -m PyInstaller \
	--noconfirm \
	--clean \
	--onedir \
	--name "${APP_NAME}" \
	--workpath "${BUILD_DIR}" \
	--specpath "${BUILD_DIR}" \
	--distpath "${DIST_DIR}" \
	--add-data "${ROOT_DIR}/default.json:." \
	--add-data "${ROOT_DIR}/highscores.json:." \
	--add-data "${ROOT_DIR}/fonts/PixelOperator-Bold.ttf:fonts" \
	--add-data "${ROOT_DIR}/src/sprites/spritesheet.png:src/sprites" \
	--add-data "${MAZEGENERATOR_FILE}:." \
	--paths "$(dirname "${MAZEGENERATOR_FILE}")" \
	--hidden-import "src.ghostia01" \
	--hidden-import "src.ghostia02" \
	--hidden-import "src.visual" \
	--hidden-import "mazegenerator" \
	"${ROOT_DIR}/pac-man.py"

echo "Copying external package files..."
mkdir -p "${PACKAGE_DIR}/src/sprites"
mkdir -p "${PACKAGE_DIR}/fonts"
mkdir -p "${PACKAGE_DIR}/docs"
mkdir -p "${PACKAGE_DIR}/_internal"

cp "${ROOT_DIR}/src/sprites/spritesheet.png" "${PACKAGE_DIR}/src/sprites/spritesheet.png"
cp "${ROOT_DIR}/fonts/PixelOperator-Bold.ttf" "${PACKAGE_DIR}/fonts/PixelOperator-Bold.ttf"
cp "${ROOT_DIR}/default.json" "${PACKAGE_DIR}/default.json"
cp "${ROOT_DIR}/highscores.json" "${PACKAGE_DIR}/highscores.json"
cp "${ROOT_DIR}/README.md" "${PACKAGE_DIR}/README.md"
cp -r "${ROOT_DIR}/docs/." "${PACKAGE_DIR}/docs/"
cp "${MAZEGENERATOR_FILE}" "${PACKAGE_DIR}/_internal/mazegenerator.py"

echo "Creating launcher script..."
cat > "${PACKAGE_DIR}/run.sh" << 'EOF'
#!/usr/bin/env sh

cd "$(dirname "$0")"
./pac-man default.json
EOF

chmod +x "${PACKAGE_DIR}/run.sh"
chmod +x "${PACKAGE_DIR}/pac-man"

echo "Creating package instructions..."
cat > "${PACKAGE_DIR}/README.txt" << 'EOF'
Pac-Man - 42 Project Package

How to run:
1. Open a terminal in this directory.
2. Run: ./run.sh

Alternative:
./pac-man default.json

If your extraction tool removes executable permissions, run:
chmod +x run.sh pac-man
./run.sh

Controls:
- Arrow keys or WASD: move Pac-Man
- P: pause / resume
- ESC: quit
- Left Shift: cheat mode / invincibility while pressed
- R: skip current level
- O: open maze / review helper mode

Configuration:
- The game uses default.json as its configuration file.
- You can edit default.json before launching the game.
- The executable must receive exactly one JSON configuration file argument.

Highscores:
- Highscores are stored in highscores.json.
- The file is kept next to default.json so it remains visible and easy to reset.

Documentation:
- The full project README is included as README.md.
- Project management documents are included in the docs directory.
EOF

if [ ! -f "${PACKAGE_DIR}/_internal/mazegenerator.py" ]; then
	echo "Error: mazegenerator was not bundled correctly." >&2
	exit 1
fi

echo "Creating ZIP package..."
python3 - << PY
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo
import stat

root = Path("${DIST_DIR}")
package = root / "${APP_NAME}"
zip_path = Path("${RELEASE_DIR}") / "${ZIP_NAME}"

with ZipFile(zip_path, "w", ZIP_DEFLATED) as archive:
    for path in package.rglob("*"):
        archive_name = path.relative_to(root)

        info = ZipInfo.from_file(path, str(archive_name))
        info.compress_type = ZIP_DEFLATED

        mode = path.stat().st_mode
        if path.name in {"run.sh", "${APP_NAME}"}:
            mode |= stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH

        info.external_attr = (mode & 0xFFFF) << 16

        if path.is_dir():
            archive.writestr(info, b"")
        else:
            with path.open("rb") as file:
                archive.writestr(info, file.read())
PY

echo "Package created successfully:"
echo "${RELEASE_DIR}/${ZIP_NAME}"
echo
echo "Test it with:"
echo "rm -rf /tmp/pac-man-test"
echo "mkdir -p /tmp/pac-man-test"
echo "python3 -m zipfile -e ${RELEASE_DIR}/${ZIP_NAME} /tmp/pac-man-test"
echo "cd /tmp/pac-man-test/${APP_NAME}"
echo "chmod +x run.sh pac-man"
echo "./run.sh"