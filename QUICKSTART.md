# Quick Start Guide for COSMOS MQTT Controller

## Building Your APK

### Option 1: Using the Build Script (Recommended)
1. Open PowerShell as Administrator
2. Navigate to the project folder:
   ```powershell
   cd "c:\Users\LENOVO\Desktop\COSMOS\mqtt-controller-app"
   ```
3. Run the build script:
   ```powershell
   .\build.bat
   ```

### Option 2: Manual Build
1. Open PowerShell in the project directory
2. Run these commands:
   ```powershell
   buildozer android debug
   ```

## Prerequisites (Auto-installed by Buildozer)
- Java JDK 8 (will be prompted to install if missing)
- Android SDK (automatically downloaded)
- Android NDK (automatically downloaded)

## Expected Build Time
- **First build**: 30-60 minutes (downloads Android SDK/NDK)
- **Subsequent builds**: 5-10 minutes

## APK Location
After successful build, find your APK at:
```
bin\cosmosmqtt-1.0-armeabi-v7a-debug.apk
```

## Installation on Android Device
1. Enable "Unknown Sources" in Android settings
2. Transfer APK to your device
3. Install the APK
4. Grant requested permissions

## App Usage
1. **Enter MQTT Credentials**:
   - Broker: `broker.hivemq.com` (or your broker)
   - Port: `1883`
   - Username/Password: (if required)

2. **Connect**: Tap "Connect to MQTT Broker"

3. **Control**:
   - Red button or Volume Up = Brake (`brakeCosmos` topic, payload `1`)
   - Green button or Volume Down = Land (`landCosmos` topic, payload `1`)

4. **Background Mode**: Enable switches for volume control and background operation

## Troubleshooting
- **Build fails**: Ensure you have internet connection for downloading Android SDK
- **Java errors**: Install Oracle JDK 8 (not OpenJDK)
- **Permission errors**: Run PowerShell as Administrator
- **App crashes**: Check Android version (minimum API 21 / Android 5.0)

## Success Indicators
✅ APK builds successfully  
✅ App installs on Android device  
✅ MQTT connection works  
✅ Commands sent to `brakeCosmos` and `landCosmos` topics  
✅ Volume buttons trigger commands  
✅ App runs in background  

Your COSMOS MQTT Controller is ready to use!
