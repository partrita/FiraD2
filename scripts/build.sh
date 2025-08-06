#!/usr/bin/env bash
set -eo pipefail

# This script replicates the logic from the original scripts/build.py

# =======================================
#  Setup Phase (from build.py setup())
# =======================================
echo "[INFO] Setting up build environment..."

# These paths are read by the python scripts from config.py
export DOWNLOAD_PATH="assets"
export BUILT_FONTS_PATH="built_fonts"

mkdir -p "$DOWNLOAD_PATH"
mkdir -p "$BUILT_FONTS_PATH"

echo "[INFO] Extracting font archives..."
# The env variables D2CODING_SRC, FIRACODE_SRC, FIRACODE_NERD_SRC
# are passed from the flake.nix derivation and point to the zip files.
unzip -o "$D2CODING_SRC" -d "$DOWNLOAD_PATH"
unzip -o "$FIRACODE_SRC" -d "$DOWNLOAD_PATH"
unzip -o "$FIRACODE_NERD_SRC" -d "$DOWNLOAD_PATH"

echo "[INFO] Cleaning up non-regular ttf files..."
find "$DOWNLOAD_PATH" -type f -name "*.ttf" | while read -r file; do
    # Keep all D2Coding TTF files
    if [[ "$file" == *D2Coding* ]]; then
        echo "  - Keeping D2Coding font file: $file"
        continue
    fi

    # For other fonts, remove non-Regular variants
    if [[ "$file" != *Regular* ]]; then
        echo "  - Removing: $file"
        rm "$file"
    fi
done

# =======================================
#  Build Phase (from build.py build())
# =======================================
echo "[INFO] Building fonts..."
# Directly call the main build function.
# The python scripts will use the environment variables we set for paths.
python3 scripts/build.py build

echo "[INFO] Build complete. Fonts are in $BUILT_FONTS_PATH"
