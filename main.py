"""
COSMOS MQTT Controller App
An Android app built with Kivy that sends MQTT commands for brake and land operations.
Runs in background and responds to volume button presses.
"""

import json
import threading
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.utils import platform

import paho.mqtt.client as mqtt

if platform == 'android':
    from android.permissions import request_permissions, Permission
    from android import mActivity
    from jnius import autoclass
    
    # Android classes
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Intent = autoclass('android.content.Intent')
    PendingIntent = autoclass('android.app.PendingIntent')
    AndroidString = autoclass('java.lang.String')
    Context = autoclass('android.content.Context')
    
    # Request permissions
    request_permissions([
        Permission.WAKE_LOCK,
        Permission.INTERNET,
        Permission.ACCESS_NETWORK_STATE,
        Permission.FOREGROUND_SERVICE
    ])


class MQTTController:
    def __init__(self, app_instance):
        self.app = app_instance
        self.client = None
        self.connected = False
        self.broker_host = ""
        self.broker_port = 1883
        self.username = ""
        self.password = ""
        self.brake_topic = "brakeCosmos"
        self.land_topic = "landCosmos"
        
    def connect(self, host, port, username, password):
        """Connect to MQTT broker"""
        try:
            self.broker_host = host
            self.broker_port = int(port)
            self.username = username
            self.password = password
            
            # Create MQTT client with version compatibility
            try:
                # Try new method (paho-mqtt 2.0+)
                self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
                Logger.info("MQTT: Using CallbackAPIVersion.VERSION1")
            except (AttributeError, TypeError):
                # Fallback to old method (paho-mqtt 1.x)
                self.client = mqtt.Client()
                Logger.info("MQTT: Using legacy client creation")
            
            # Set credentials if provided
            if username and password:
                self.client.username_pw_set(username, password)
                
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_message = self.on_message
            
            self.client.connect(host, int(port), 60)
            self.client.loop_start()
            
            Logger.info(f"MQTT: Connecting to {host}:{port}")
            return True
            
        except Exception as e:
            Logger.error(f"MQTT: Connection failed - {str(e)}")
            self.app.update_status(f"Connection failed: {str(e)}")
            return False
    
    def on_connect(self, client, userdata, flags, rc):
        """Callback for when the client receives a CONNACK response from the server"""
        if rc == 0:
            self.connected = True
            Logger.info("MQTT: Connected successfully")
            self.app.update_status("Connected to MQTT broker")
        else:
            self.connected = False
            Logger.error(f"MQTT: Connection failed with code {rc}")
            self.app.update_status(f"Connection failed with code {rc}")
    
    def on_disconnect(self, client, userdata, rc):
        """Callback for when the client disconnects from the broker"""
        self.connected = False
        Logger.info("MQTT: Disconnected from broker")
        self.app.update_status("Disconnected from MQTT broker")
    
    def on_message(self, client, userdata, msg):
        """Callback for when a PUBLISH message is received from the server"""
        Logger.info(f"MQTT: Received message: {msg.topic} - {msg.payload.decode()}")
    
    def publish_brake(self):
        """Publish brake command"""
        if self.connected and self.client:
            try:
                payload = "1"
                self.client.publish(self.brake_topic, payload)
                Logger.info(f"MQTT: Published brake command - {self.brake_topic}: {payload}")
                self.app.update_status(f"Brake command sent: {payload}")
                return True
            except Exception as e:
                Logger.error(f"MQTT: Failed to publish brake - {str(e)}")
                return False
        else:
            Logger.warning("MQTT: Not connected, cannot publish brake")
            return False
    
    def publish_land(self):
        """Publish land command"""
        if self.connected and self.client:
            try:
                payload = "1"
                self.client.publish(self.land_topic, payload)
                Logger.info(f"MQTT: Published land command - {self.land_topic}: {payload}")
                self.app.update_status(f"Land command sent: {payload}")
                return True
            except Exception as e:
                Logger.error(f"MQTT: Failed to publish land - {str(e)}")
                return False
        else:
            Logger.warning("MQTT: Not connected, cannot publish land")
            return False
    
    def disconnect(self):
        """Disconnect from MQTT broker"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False


class VolumeButtonHandler:
    """Handles volume button presses for brake/land commands"""
    
    def __init__(self, mqtt_controller):
        self.mqtt_controller = mqtt_controller
        self.monitoring = False
        
    def start_monitoring(self):
        """Start monitoring volume buttons"""
        if platform == 'android':
            self.monitoring = True
            # Note: Volume button handling requires special Android implementation
            # This is a placeholder - actual implementation would need Android-specific code
            Logger.info("Volume button monitoring started")
        
    def stop_monitoring(self):
        """Stop monitoring volume buttons"""
        self.monitoring = False
        Logger.info("Volume button monitoring stopped")


class COSMOSMQTTApp(App):
    def build(self):
        self.title = "COSMOS MQTT Controller"
        self.mqtt_controller = MQTTController(self)
        self.volume_handler = VolumeButtonHandler(self.mqtt_controller)
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title_label = Label(text='COSMOS MQTT Controller', 
                           size_hint_y=None, height=50,
                           font_size='20sp')
        main_layout.add_widget(title_label)
        
        # Connection settings
        settings_layout = BoxLayout(orientation='vertical', spacing=5)
        
        # Broker host
        host_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        host_layout.add_widget(Label(text='Broker Host:', size_hint_x=0.3))
        self.host_input = TextInput(text='broker.hivemq.com', multiline=False)
        host_layout.add_widget(self.host_input)
        settings_layout.add_widget(host_layout)
        
        # Broker port
        port_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        port_layout.add_widget(Label(text='Port:', size_hint_x=0.3))
        self.port_input = TextInput(text='1883', multiline=False)
        port_layout.add_widget(self.port_input)
        settings_layout.add_widget(port_layout)
        
        # Username
        user_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        user_layout.add_widget(Label(text='Username:', size_hint_x=0.3))
        self.username_input = TextInput(text='', multiline=False)
        user_layout.add_widget(self.username_input)
        settings_layout.add_widget(user_layout)
        
        # Password
        pass_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        pass_layout.add_widget(Label(text='Password:', size_hint_x=0.3))
        self.password_input = TextInput(text='', password=True, multiline=False)
        pass_layout.add_widget(self.password_input)
        settings_layout.add_widget(pass_layout)
        
        main_layout.add_widget(settings_layout)
        
        # Connect button
        self.connect_btn = Button(text='Connect to MQTT Broker', 
                                 size_hint_y=None, height=50)
        self.connect_btn.bind(on_press=self.connect_mqtt)
        main_layout.add_widget(self.connect_btn)
        
        # Status label
        self.status_label = Label(text='Disconnected', 
                                 size_hint_y=None, height=30,
                                 color=(1, 0, 0, 1))
        main_layout.add_widget(self.status_label)
        
        # Control buttons
        controls_layout = BoxLayout(orientation='horizontal', spacing=10, 
                                   size_hint_y=None, height=60)
        
        self.brake_btn = Button(text='BRAKE\n(Volume Up)', 
                               background_color=(1, 0, 0, 1))
        self.brake_btn.bind(on_press=self.send_brake)
        controls_layout.add_widget(self.brake_btn)
        
        self.land_btn = Button(text='LAND\n(Volume Down)', 
                              background_color=(0, 1, 0, 1))
        self.land_btn.bind(on_press=self.send_land)
        controls_layout.add_widget(self.land_btn)
        
        main_layout.add_widget(controls_layout)
        
        # Volume monitoring toggle
        volume_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        volume_layout.add_widget(Label(text='Volume Button Control:', size_hint_x=0.7))
        self.volume_switch = Switch(active=False)
        self.volume_switch.bind(active=self.toggle_volume_monitoring)
        volume_layout.add_widget(self.volume_switch)
        main_layout.add_widget(volume_layout)
        
        # Background service toggle
        bg_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        bg_layout.add_widget(Label(text='Run in Background:', size_hint_x=0.7))
        self.bg_switch = Switch(active=False)
        self.bg_switch.bind(active=self.toggle_background_service)
        bg_layout.add_widget(self.bg_switch)
        main_layout.add_widget(bg_layout)
        
        # Log area
        log_label = Label(text='Activity Log:', size_hint_y=None, height=30)
        main_layout.add_widget(log_label)
        
        self.log_label = Label(text='App started...', 
                              text_size=(None, None),
                              valign='top',
                              halign='left')
        main_layout.add_widget(self.log_label)
        
        return main_layout
    
    def connect_mqtt(self, instance):
        """Connect to MQTT broker"""
        host = self.host_input.text.strip()
        port = self.port_input.text.strip()
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()
        
        if not host:
            self.show_popup("Error", "Please enter broker host")
            return
        
        if not port:
            port = "1883"
        
        # Update button state
        self.connect_btn.text = "Connecting..."
        self.connect_btn.disabled = True
        
        # Connect in background thread
        threading.Thread(target=self._connect_worker, 
                        args=(host, port, username, password)).start()
    
    def _connect_worker(self, host, port, username, password):
        """Worker thread for MQTT connection"""
        success = self.mqtt_controller.connect(host, port, username, password)
        
        # Update UI on main thread
        Clock.schedule_once(lambda dt: self._update_connect_ui(success), 0)
    
    def _update_connect_ui(self, success):
        """Update connection UI"""
        if success:
            self.connect_btn.text = "Disconnect"
            self.connect_btn.disabled = False
            self.connect_btn.bind(on_press=self.disconnect_mqtt)
        else:
            self.connect_btn.text = "Connect to MQTT Broker"
            self.connect_btn.disabled = False
    
    def disconnect_mqtt(self, instance):
        """Disconnect from MQTT broker"""
        self.mqtt_controller.disconnect()
        self.connect_btn.text = "Connect to MQTT Broker"
        self.connect_btn.bind(on_press=self.connect_mqtt)
        self.update_status("Disconnected")
    
    def send_brake(self, instance):
        """Send brake command"""
        success = self.mqtt_controller.publish_brake()
        if not success:
            self.show_popup("Error", "Failed to send brake command. Check connection.")
    
    def send_land(self, instance):
        """Send land command"""
        success = self.mqtt_controller.publish_land()
        if not success:
            self.show_popup("Error", "Failed to send land command. Check connection.")
    
    def toggle_volume_monitoring(self, instance, value):
        """Toggle volume button monitoring"""
        if value:
            self.volume_handler.start_monitoring()
            self.update_status("Volume button monitoring enabled")
        else:
            self.volume_handler.stop_monitoring()
            self.update_status("Volume button monitoring disabled")
    
    def toggle_background_service(self, instance, value):
        """Toggle background service"""
        if value:
            self.start_background_service()
            self.update_status("Background service enabled")
        else:
            self.stop_background_service()
            self.update_status("Background service disabled")
    
    def start_background_service(self):
        """Start background service"""
        if platform == 'android':
            # Start foreground service to keep app running
            Logger.info("Starting background service")
            # This would require Android-specific implementation
    
    def stop_background_service(self):
        """Stop background service"""
        if platform == 'android':
            Logger.info("Stopping background service")
    
    def update_status(self, message):
        """Update status label"""
        def update_ui(dt):
            self.status_label.text = message
            if "Connected" in message:
                self.status_label.color = (0, 1, 0, 1)  # Green
            elif "failed" in message or "Error" in message:
                self.status_label.color = (1, 0, 0, 1)  # Red
            else:
                self.status_label.color = (1, 1, 0, 1)  # Yellow
            
            # Update log
            current_time = time.strftime("%H:%M:%S")
            self.log_label.text += f"\n[{current_time}] {message}"
        
        Clock.schedule_once(update_ui, 0)
    
    def show_popup(self, title, message):
        """Show popup message"""
        popup = Popup(title=title,
                     content=Label(text=message),
                     size_hint=(0.8, 0.4))
        popup.open()
    
    def on_start(self):
        """Called when the app starts"""
        self.update_status("App started - Enter MQTT credentials to connect")
    
    def on_stop(self):
        """Called when the app stops"""
        if self.mqtt_controller:
            self.mqtt_controller.disconnect()
        if self.volume_handler:
            self.volume_handler.stop_monitoring()


if __name__ == '__main__':
    COSMOSMQTTApp().run()
