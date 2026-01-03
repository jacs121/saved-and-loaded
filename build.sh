#!/bin/bash

PLATFORM=$1

if [ "$PLATFORM" = "windows" ]; then
    pyinstaller --noconfirm --onefile --noconsole \
        --name "Saved-And-Loaded-windows" \
        --clean main.py

elif [ "$PLATFORM" = "linux" ]; then
    pip install --no-input pyvirtualcam
    pyinstaller --noconfirm --onefile --noconsole \
        --name "Saved-And-Loaded-linux.exe" \
        --noupx \
        --clean main.py

elif [ "$PLATFORM" = "macos" ]; then
    pyinstaller --noconfirm --onefile --noconsole \
        --name "Saved-And-Loaded-macos.exe" \
        --clean main.py

else
    echo "Usage: build.sh [windows|linux|macos]"
    exit 1
fi