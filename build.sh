#!/bin/bash

# COSMOS MQTT Controller - Build Script
# This script automates the APK building process

echo "=== COSMOS MQTT Controller Build Script ==="
echo ""

# Check if Python is installed
echo "Checking Python installation..."
python --version
if [ $? -ne 0 ]; then
    echo "Error: Python is not installed or not in PATH"
    exit 1
fi

# Check if pip is available
echo "Checking pip installation..."
pip --version
if [ $? -ne 0 ]; then
    echo "Error: pip is not installed or not in PATH"
    exit 1
fi

# Install buildozer if not present
echo "Installing/Upgrading Buildozer..."
pip install --upgrade buildozer

# Install requirements
echo "Installing Python requirements..."
pip install -r requirements.txt

# Clean previous builds (optional)
echo "Cleaning previous builds..."
buildozer android clean

# Build the APK
echo "Building APK (this may take a while on first run)..."
buildozer android debug

# Check if build was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "=== BUILD SUCCESSFUL ==="
    echo "APK location: bin/cosmosmqtt-1.0-armeabi-v7a-debug.apk"
    echo ""
    echo "To install on device:"
    echo "1. Enable 'Unknown Sources' in Android settings"
    echo "2. Transfer APK to device"
    echo "3. Install the APK"
    echo ""
    echo "For release build, run: buildozer android release"
else
    echo ""
    echo "=== BUILD FAILED ==="
    echo "Check the error messages above for troubleshooting"
    echo "Common issues:"
    echo "- Java JDK not installed (need JDK 8)"
    echo "- Android SDK issues (let buildozer download it)"
    echo "- Network issues downloading dependencies"
fi
