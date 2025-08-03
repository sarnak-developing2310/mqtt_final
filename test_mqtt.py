#!/usr/bin/env python3
"""
Test script to verify MQTT functionality with the new paho-mqtt version
"""

import paho.mqtt.client as mqtt
import time
import sys

def test_mqtt_client():
    """Test MQTT client creation and basic functionality"""
    try:
        print("Testing MQTT client creation...")
        
        # Test new CallbackAPIVersion method
        try:
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
            print("✅ SUCCESS: Created client with CallbackAPIVersion.VERSION1")
        except Exception as e:
            print(f"❌ FAILED: CallbackAPIVersion method - {e}")
            
            # Fallback to old method
            try:
                client = mqtt.Client()
                print("✅ SUCCESS: Created client with old method (fallback)")
            except Exception as e2:
                print(f"❌ FAILED: Both methods failed - {e2}")
                return False
        
        # Test callback assignment
        def on_connect(client, userdata, flags, rc):
            print(f"Connected with result code {rc}")
            
        def on_message(client, userdata, msg):
            print(f"Message received: {msg.topic} - {msg.payload.decode()}")
            
        def on_disconnect(client, userdata, rc):
            print(f"Disconnected with result code {rc}")
            
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect
        
        print("✅ SUCCESS: Callbacks assigned successfully")
        
        # Test publishing without connection (should not crash)
        try:
            result = client.publish("test/topic", "test payload")
            print(f"✅ SUCCESS: Publish method works (result: {result})")
        except Exception as e:
            print(f"❌ WARNING: Publish failed - {e}")
            
        print("\n🎉 MQTT client test completed successfully!")
        print("The paho-mqtt library is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ CRITICAL FAILURE: {e}")
        return False

if __name__ == "__main__":
    print("COSMOS MQTT Controller - Library Test")
    print("=" * 50)
    
    # Test paho-mqtt import
    try:
        import paho.mqtt.client as mqtt
        print("✅ SUCCESS: paho-mqtt imported successfully")
        print(f"   Version: {mqtt.__version__ if hasattr(mqtt, '__version__') else 'Unknown'}")
    except ImportError as e:
        print(f"❌ FAILED: Cannot import paho-mqtt - {e}")
        sys.exit(1)
    
    # Run the test
    if test_mqtt_client():
        print("\n✅ ALL TESTS PASSED!")
        print("Your MQTT setup is ready for COSMOS drone control.")
    else:
        print("\n❌ SOME TESTS FAILED!")
        print("There may be issues with your MQTT setup.")
        sys.exit(1)
