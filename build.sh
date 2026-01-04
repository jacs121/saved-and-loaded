#!/bin/bash

PLATFORM=$1

# Install dependencies
pip install --no-input pyinstaller

if [ "$PLATFORM" = "windows" ]; then
    pyinstaller --noconfirm --onefile \
        --name "Saved-And-Loaded-windows" \
        --clean main.py

elif [ "$PLATFORM" = "macos" ]; then
    pyinstaller --noconfirm --onefile \
        --name "Saved-And-Loaded-macos.exe" \
        --clean main.py

else
    echo "Usage: build.sh [windows|macos]"
    exit 1
fi