# 📱 COSMOS MQTT Controller - Pydroid 3 Setup Guide

## Quick Setup for Pydroid 3 (Android)

### Step 1: Install Pydroid 3
1. Download **Pydroid 3** from Google Play Store
2. Open the app and wait for Python to initialize

### Step 2: Install Required Package
1. In Pydroid 3, tap the **menu** (3 lines) → **Pip**
2. Search for and install: `paho-mqtt`
3. Wait for installation to complete

### Step 3: Download the Code
1. **Option A**: Copy `cosmos_mqtt_controller.py` to your device
2. **Option B**: Download from GitHub: https://github.com/sarnak-developing2310/mqtt_final

### Step 4: Run the App
1. Open `cosmos_mqtt_controller.py` in Pydroid 3
2. Tap the **Play** button ▶️
3. The COSMOS MQTT Controller window will appear

## 🎮 Using the App

### Connection Setup
1. **Broker Host**: Enter your MQTT broker (default: `broker.hivemq.com`)
2. **Port**: Usually `1883` for non-SSL
3. **Username/Password**: If required by your broker
4. Tap **"Connect to MQTT Broker"**

### Control Commands
- 🛑 **Red BRAKE Button**: Emergency brake (`brakeCosmos` topic)
- 🛬 **Green LAND Button**: Safe landing (`landCosmos` topic)
- Both send payload `"1"` to respective topics

### Keyboard Shortcuts (if supported)
- `Ctrl+B`: Send brake command
- `Ctrl+L`: Send land command  
- `Ctrl+Q`: Quit application

## 📋 Features

✅ **Single File**: Everything in one Python file  
✅ **Pydroid 3 Compatible**: Runs perfectly on Android  
✅ **Desktop Compatible**: Also works on Windows/Mac/Linux  
✅ **Real-time Logging**: See all activity in the log window  
✅ **Visual Feedback**: Button animation on command send  
✅ **Error Handling**: Clear error messages and warnings  
✅ **Connection Status**: Always know if you're connected  

## 🔧 Troubleshooting

### "Module not found" error
- Make sure you installed `paho-mqtt` via Pip in Pydroid 3

### Connection issues
- Check your internet connection
- Try public broker: `broker.hivemq.com:1883`
- Verify broker address and port

### App not responding
- Close and restart Pydroid 3
- Make sure your device has enough RAM

## 🚁 Ready to Control Your COSMOS Drone!

Your single-file MQTT controller is ready. Just run it in Pydroid 3 and start controlling your drone with simple button taps!

**File to run**: `cosmos_mqtt_controller.py`  
**Topics**: `brakeCosmos` and `landCosmos`  
**Payload**: `"1"` for both commands
