@echo off
REM COSMOS MQTT Controller - Windows Build Script
REM This script automates the APK building process on Windows

echo === COSMOS MQTT Controller Build Script ===
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if pip is available
echo Checking pip installation...
python -m pip --version
if %errorlevel% neq 0 (
    echo Error: pip is not installed or not in PATH
    pause
    exit /b 1
)

REM Install buildozer if not present
echo Installing/Upgrading Buildozer...
python -m pip install --upgrade buildozer

REM Install requirements
echo Installing Python requirements...
python -m pip install -r requirements.txt

REM Clean previous builds (optional)
echo Cleaning previous builds...
python -m buildozer android clean

REM Build the APK
echo Building APK (this may take a while on first run)...
python -m buildozer android debug

REM Check if build was successful
if %errorlevel% equ 0 (
    echo.
    echo === BUILD SUCCESSFUL ===
    echo APK location: bin\cosmosmqtt-1.0-armeabi-v7a-debug.apk
    echo.
    echo To install on device:
    echo 1. Enable 'Unknown Sources' in Android settings
    echo 2. Transfer APK to device
    echo 3. Install the APK
    echo.
    echo For release build, run: buildozer android release
) else (
    echo.
    echo === BUILD FAILED ===
    echo Check the error messages above for troubleshooting
    echo Common issues:
    echo - Java JDK not installed (need JDK 8)
    echo - Android SDK issues (let buildozer download it)
    echo - Network issues downloading dependencies
)

pause
