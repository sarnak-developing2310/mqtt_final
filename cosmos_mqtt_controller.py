"""
COSMOS MQTT Controller - Pydroid 3 Compatible Version
A single-file Python app for controlling COSMOS drones via MQTT.
Optimized for Pydroid 3 on Android devices.
"""

import json
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import paho.mqtt.client as mqtt


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
            
            self.client = mqtt.Client()
            if username and password:
                self.client.username_pw_set(username, password)
            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_message = self.on_message
            
            self.client.connect(host, int(port), 60)
            self.client.loop_start()
            
            self.app.log_message(f"MQTT: Connecting to {host}:{port}")
            return True
            
        except Exception as e:
            self.app.log_message(f"Connection failed: {str(e)}")
            return False
    
    def on_connect(self, client, userdata, flags, rc):
        """Callback for when the client receives a CONNACK response from the server"""
        if rc == 0:
            self.connected = True
            self.app.log_message("✅ Connected to MQTT broker")
            self.app.update_connection_status(True)
        else:
            self.connected = False
            self.app.log_message(f"❌ Connection failed with code {rc}")
            self.app.update_connection_status(False)
    
    def on_disconnect(self, client, userdata, rc):
        """Callback for when the client disconnects from the broker"""
        self.connected = False
        self.app.log_message("📡 Disconnected from MQTT broker")
        self.app.update_connection_status(False)
    
    def on_message(self, client, userdata, msg):
        """Callback for when a PUBLISH message is received from the server"""
        self.app.log_message(f"📨 Received: {msg.topic} - {msg.payload.decode()}")
    
    def publish_brake(self):
        """Publish brake command"""
        if self.connected and self.client:
            try:
                payload = "1"
                self.client.publish(self.brake_topic, payload)
                self.app.log_message(f"🛑 BRAKE command sent: {self.brake_topic} = {payload}")
                return True
            except Exception as e:
                self.app.log_message(f"❌ Failed to send brake: {str(e)}")
                return False
        else:
            self.app.log_message("⚠️ Not connected, cannot send brake command")
            return False
    
    def publish_land(self):
        """Publish land command"""
        if self.connected and self.client:
            try:
                payload = "1"
                self.client.publish(self.land_topic, payload)
                self.app.log_message(f"🛬 LAND command sent: {self.land_topic} = {payload}")
                return True
            except Exception as e:
                self.app.log_message(f"❌ Failed to send land: {str(e)}")
                return False
        else:
            self.app.log_message("⚠️ Not connected, cannot send land command")
            return False
    
    def disconnect(self):
        """Disconnect from MQTT broker"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False


class COSMOSMQTTApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚁 COSMOS MQTT Controller")
        self.root.geometry("400x600")
        self.root.configure(bg='#2c3e50')
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.mqtt_controller = MQTTController(self)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='#2c3e50', padx=20, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="🚁 COSMOS MQTT Controller", 
                              font=('Arial', 16, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(pady=10)
        
        # Connection frame
        conn_frame = tk.LabelFrame(main_frame, text="MQTT Connection", 
                                  font=('Arial', 12, 'bold'), fg='white', bg='#34495e')
        conn_frame.pack(fill=tk.X, pady=10)
        
        # Broker host
        tk.Label(conn_frame, text="Broker Host:", fg='white', bg='#34495e').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.host_entry = tk.Entry(conn_frame, width=25)
        self.host_entry.insert(0, "broker.hivemq.com")
        self.host_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Port
        tk.Label(conn_frame, text="Port:", fg='white', bg='#34495e').grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.port_entry = tk.Entry(conn_frame, width=25)
        self.port_entry.insert(0, "1883")
        self.port_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Username
        tk.Label(conn_frame, text="Username:", fg='white', bg='#34495e').grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.username_entry = tk.Entry(conn_frame, width=25)
        self.username_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Password
        tk.Label(conn_frame, text="Password:", fg='white', bg='#34495e').grid(row=3, column=0, sticky='w', padx=5, pady=5)
        self.password_entry = tk.Entry(conn_frame, width=25, show="*")
        self.password_entry.grid(row=3, column=1, padx=5, pady=5)
        
        # Connect button
        self.connect_btn = tk.Button(main_frame, text="🔗 Connect to MQTT Broker", 
                                   font=('Arial', 12, 'bold'), bg='#3498db', fg='white',
                                   command=self.toggle_connection)
        self.connect_btn.pack(pady=10, fill=tk.X)
        
        # Status
        self.status_label = tk.Label(main_frame, text="❌ Disconnected", 
                                   font=('Arial', 11), fg='#e74c3c', bg='#2c3e50')
        self.status_label.pack(pady=5)
        
        # Control buttons frame
        controls_frame = tk.Frame(main_frame, bg='#2c3e50')
        controls_frame.pack(pady=15)
        
        # Brake button
        self.brake_btn = tk.Button(controls_frame, text="🛑 EMERGENCY\nBRAKE", 
                                 font=('Arial', 14, 'bold'), bg='#e74c3c', fg='white',
                                 width=12, height=3, command=self.send_brake)
        self.brake_btn.pack(side=tk.LEFT, padx=10)
        
        # Land button
        self.land_btn = tk.Button(controls_frame, text="🛬 SAFE\nLAND", 
                                font=('Arial', 14, 'bold'), bg='#27ae60', fg='white',
                                width=12, height=3, command=self.send_land)
        self.land_btn.pack(side=tk.RIGHT, padx=10)
        
        # Topics info
        topics_frame = tk.LabelFrame(main_frame, text="MQTT Topics", 
                                   font=('Arial', 10, 'bold'), fg='white', bg='#34495e')
        topics_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(topics_frame, text="🛑 Brake: brakeCosmos (payload: '1')", 
                fg='white', bg='#34495e').pack(anchor='w', padx=5, pady=2)
        tk.Label(topics_frame, text="🛬 Land: landCosmos (payload: '1')", 
                fg='white', bg='#34495e').pack(anchor='w', padx=5, pady=2)
        
        # Log area
        log_frame = tk.LabelFrame(main_frame, text="Activity Log", 
                                font=('Arial', 10, 'bold'), fg='white', bg='#34495e')
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=50,
                                                bg='#1a252f', fg='#ecf0f1', 
                                                font=('Consolas', 9))
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Initial log message
        self.log_message("🚀 COSMOS MQTT Controller started")
        self.log_message("📝 Enter MQTT broker details and click Connect")
        
    def log_message(self, message):
        """Add a timestamped message to the log"""
        timestamp = time.strftime("[%H:%M:%S]")
        log_entry = f"{timestamp} {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
    def update_connection_status(self, connected):
        """Update the connection status display"""
        if connected:
            self.status_label.config(text="✅ Connected", fg='#27ae60')
            self.connect_btn.config(text="🔌 Disconnect", bg='#e74c3c')
        else:
            self.status_label.config(text="❌ Disconnected", fg='#e74c3c')
            self.connect_btn.config(text="🔗 Connect to MQTT Broker", bg='#3498db')
    
    def toggle_connection(self):
        """Toggle MQTT connection"""
        if self.mqtt_controller.connected:
            self.mqtt_controller.disconnect()
            self.log_message("🔌 Disconnecting from MQTT broker...")
        else:
            host = self.host_entry.get().strip()
            port = self.port_entry.get().strip()
            username = self.username_entry.get().strip()
            password = self.password_entry.get().strip()
            
            if not host:
                messagebox.showerror("Error", "Please enter broker host")
                return
            
            if not port:
                port = "1883"
            
            self.log_message(f"🔗 Connecting to {host}:{port}...")
            self.connect_btn.config(text="⏳ Connecting...", state='disabled')
            
            # Connect in background thread
            def connect_worker():
                success = self.mqtt_controller.connect(host, port, username, password)
                # Re-enable button
                self.root.after(100, lambda: self.connect_btn.config(state='normal'))
                if not success:
                    self.root.after(100, lambda: self.update_connection_status(False))
            
            threading.Thread(target=connect_worker, daemon=True).start()
    
    def send_brake(self):
        """Send brake command"""
        if not self.mqtt_controller.connected:
            messagebox.showwarning("Warning", "Not connected to MQTT broker!")
            return
        
        success = self.mqtt_controller.publish_brake()
        if success:
            # Visual feedback
            original_color = self.brake_btn.cget('bg')
            self.brake_btn.config(bg='#c0392b')
            self.root.after(200, lambda: self.brake_btn.config(bg=original_color))
        else:
            messagebox.showerror("Error", "Failed to send brake command")
    
    def send_land(self):
        """Send land command"""
        if not self.mqtt_controller.connected:
            messagebox.showwarning("Warning", "Not connected to MQTT broker!")
            return
        
        success = self.mqtt_controller.publish_land()
        if success:
            # Visual feedback
            original_color = self.land_btn.cget('bg')
            self.land_btn.config(bg='#1e8449')
            self.root.after(200, lambda: self.land_btn.config(bg=original_color))
        else:
            messagebox.showerror("Error", "Failed to send land command")
    
    def on_closing(self):
        """Handle application closing"""
        if self.mqtt_controller.connected:
            self.mqtt_controller.disconnect()
        self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Add keyboard shortcuts
        self.root.bind('<Control-b>', lambda e: self.send_brake())
        self.root.bind('<Control-l>', lambda e: self.send_land())
        self.root.bind('<Control-q>', lambda e: self.on_closing())
        
        self.log_message("⌨️ Keyboard shortcuts: Ctrl+B (Brake), Ctrl+L (Land), Ctrl+Q (Quit)")
        
        self.root.mainloop()


if __name__ == '__main__':
    print("🚁 Starting COSMOS MQTT Controller...")
    print("📱 Compatible with Pydroid 3 and desktop Python")
    print("🔗 Connect to your MQTT broker and control your COSMOS drone!")
    
    app = COSMOSMQTTApp()
    app.run()
