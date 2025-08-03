# COSMOS MQTT Controller 🚁

An Android app that controls COSMOS drones via MQTT commands. Built with Python/Kivy and automatically compiled to APK using GitHub Actions.

## 🚀 Features

- **🔗 MQTT Connection**: Connect to any MQTT broker with custom credentials
- **🛑 Brake Command**: Emergency brake via button or volume up key  
- **🛬 Land Command**: Safe landing via button or volume down key
- **📱 Mobile Ready**: Native Android app with intuitive interface
- **🔄 Background Mode**: Continues operating when screen is off
- **📊 Real-time Monitoring**: Live status updates and command feedback
- **🎛️ Volume Control**: Hardware volume buttons for quick commands

## 📥 Download APK

### Option 1: Latest Release (Recommended)
Go to [Releases](../../releases) and download the latest APK file.

### Option 2: Latest Build Artifacts
1. Go to [Actions](../../actions)
2. Click on the latest successful build
3. Download the APK from artifacts sectionTT Controller

An Android app built with Python/Kivy that sends MQTT commands for drone brake and land operations. The app can run in the background and respond to volume button presses.

## Features

- **MQTT Control**: Connect to any MQTT broker with custom credentials
- **Brake & Land Commands**: Send commands to `brakeCosmos` and `landCosmos` topics with payload "1"
- **Volume Button Control**: Use volume up for brake, volume down for land
- **Background Operation**: Continues running when screen is off
- **User-friendly Interface**: Easy setup and monitoring

## Topics

- **Brake Topic**: `brakeCosmos` (triggered by app button or volume up)
- **Land Topic**: `landCosmos` (triggered by app button or volume down)
- **Payload**: `1` (sent for both commands)

## Setup Instructions

### Prerequisites

1. **Install Python** (3.8 or higher)
2. **Install Java Development Kit (JDK 8)**
3. **Install Android SDK** or let Buildozer handle it automatically

### Building the APK

1. **Install Buildozer**:
   ```bash
   pip install buildozer
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize Buildozer** (first time only):
   ```bash
   buildozer init
   ```

4. **Build APK**:
   ```bash
   buildozer android debug
   ```

   For release version:
   ```bash
   buildozer android release
   ```

### Installation

1. The APK file will be generated in the `bin/` directory
2. Transfer the APK to your Android device
3. Enable "Unknown Sources" in Android settings
4. Install the APK

## Usage

### First Setup

1. **Open the app**
2. **Enter MQTT Broker Details**:
   - Broker Host (e.g., `broker.hivemq.com`)
   - Port (default: `1883`)
   - Username (if required)
   - Password (if required)
3. **Tap "Connect to MQTT Broker"**

### Controls

1. **Manual Control**:
   - Red "BRAKE" button for emergency brake
   - Green "LAND" button for landing

2. **Volume Button Control**:
   - Enable "Volume Button Control" switch
   - Volume Up = Brake command
   - Volume Down = Land command

3. **Background Operation**:
   - Enable "Run in Background" switch
   - App will continue working even when screen is off

### Status Monitoring

- **Connection Status**: Shows green when connected, red when disconnected
- **Activity Log**: Real-time log of all actions and status changes
- **Command Feedback**: Confirmation when commands are sent successfully

## Configuration

### MQTT Settings

- **Default Broker**: `broker.hivemq.com` (free public broker)
- **Default Port**: `1883`
- **Topics**: 
  - `brakeCosmos` for brake commands
  - `landCosmos` for land commands
- **Payload**: Always sends `"1"`

### Android Permissions

The app requests these permissions:
- `INTERNET` - For MQTT connection
- `ACCESS_NETWORK_STATE` - Check network status
- `WAKE_LOCK` - Keep app running in background
- `FOREGROUND_SERVICE` - Background operation

## Troubleshooting

### Build Issues

1. **Java/Android SDK Issues**:
   - Ensure JDK 8 is installed
   - Let Buildozer download Android SDK automatically
   - Check `buildozer.spec` for correct API versions

2. **Permission Errors**:
   - Run PowerShell as Administrator
   - Ensure antivirus isn't blocking files

3. **Dependencies**:
   ```bash
   pip install --upgrade buildozer
   pip install --upgrade kivy
   ```

### Runtime Issues

1. **MQTT Connection Failed**:
   - Check internet connection
   - Verify broker host and port
   - Try public brokers like `broker.hivemq.com`

2. **Volume Buttons Not Working**:
   - Enable volume button control in app
   - Grant all requested permissions
   - Some Android versions may require additional setup

3. **App Stops in Background**:
   - Enable background operation
   - Check Android battery optimization settings
   - Add app to battery whitelist

## Development

### File Structure

```
mqtt-controller-app/
├── main.py              # Main application code
├── requirements.txt     # Python dependencies
├── buildozer.spec      # Build configuration
└── README.md           # This file
```

### Key Components

- **MQTTController**: Handles MQTT connection and messaging
- **VolumeButtonHandler**: Manages volume button events
- **COSMOSMQTTApp**: Main Kivy application with UI

### Customization

To modify topics or payloads, edit these variables in `main.py`:

```python
self.brake_topic = "brakeCosmos"
self.land_topic = "landCosmos"
payload = "1"  # In publish_brake() and publish_land() methods
```

## License

This project is open source. Feel free to modify and distribute.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Android logs: `adb logcat | grep python`
3. Test MQTT connection with other clients first
