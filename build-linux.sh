#!/bin/bash

# COSMOS MQTT Controller - WSL/Linux Build Script
# Run this script in WSL or Linux to build the Android APK

echo "=== COSMOS MQTT Controller - Linux Build ==="
echo ""

# Update system
echo "Updating system packages..."
sudo apt update

# Install required dependencies
echo "Installing build dependencies..."
sudo apt install -y \
    git \
    zip \
    unzip \
    openjdk-8-jdk \
    python3-pip \
    autoconf \
    libtool \
    pkg-config \
    zlib1g-dev \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    build-essential \
    ccache

# Set JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
echo "JAVA_HOME set to: $JAVA_HOME"

# Install Python build tools
echo "Installing Python build tools..."
pip3 install --user buildozer cython

# Add local bin to PATH
export PATH=$PATH:~/.local/bin

# Clean any previous builds
echo "Cleaning previous builds..."
if [ -d ".buildozer" ]; then
    rm -rf .buildozer
fi

if [ -d "bin" ]; then
    rm -rf bin
fi

# Build the APK
echo "Building Android APK (this will take 30-60 minutes on first run)..."
echo "Please be patient while dependencies are downloaded..."

buildozer android debug

# Check if build was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "=== BUILD SUCCESSFUL ==="
    echo "APK created: bin/cosmosmqtt-1.0-armeabi-v7a-debug.apk"
    echo ""
    echo "File size:"
    ls -lh bin/*.apk
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
    echo "Check the error messages above"
    echo "Common issues:"
    echo "- Network connectivity for downloading Android SDK"
    echo "- Insufficient disk space (need ~5GB free)"
    echo "- Missing system dependencies"
    echo ""
    echo "Try running again - sometimes dependencies need multiple attempts"
fi
