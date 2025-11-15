from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.clock import Clock
import requests
import json
from threading import Thread
import time

SIGNALING_SERVER = 'http://192.168.0.3:8080'
DEVICE_ID = 'receiver_device_001'
ALLOWED_CALLER = 'caller_device_001'

class ReceiverApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connected = False
        self.in_call = False
        self.check_interval = None
        
    def build(self):
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.CAMERA,
            Permission.RECORD_AUDIO,
            Permission.INTERNET,
            Permission.WAKE_LOCK
        ])
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Status label
        self.status_label = Label(
            text='Status: Initializing...',
            size_hint=(1, 0.15),
            font_size='16sp',
            color=(1, 1, 1, 1)
        )
        layout.add_widget(self.status_label)
        
        # Device ID label
        self.device_label = Label(
            text=f'Device ID: {DEVICE_ID}',
            size_hint=(1, 0.1),
            font_size='14sp',
            color=(0.7, 0.7, 0.7, 1)
        )
        layout.add_widget(self.device_label)
        
        # Camera preview (for sending video back to caller)
        self.camera = Camera(
            play=False,
            resolution=(640, 480),
            size_hint=(1, 0.5)
        )
        layout.add_widget(self.camera)
        
        # Remote video placeholder (will show caller's video in full implementation)
        self.remote_video = Image(
            size_hint=(1, 0.25),
            allow_stretch=True,
            keep_ratio=True
        )
        layout.add_widget(self.remote_video)
        
        # Auto-connect on startup
        Clock.schedule_once(lambda dt: self.auto_connect(), 2)
        
        return layout
    
    def auto_connect(self):
        """Automatically connect to signaling server on startup"""
        self.status_label.text = 'Status: Connecting to server...'
        Thread(target=self._connect_thread).start()
    
    def _connect_thread(self):
        """Connect to signaling server and register"""
        try:
            # Test server connectivity
            response = requests.get(SIGNALING_SERVER, timeout=5)
            
            # Register device
            register_data = {
                'device_id': DEVICE_ID,
                'type': 'receiver',
                'auto_accept_from': ALLOWED_CALLER
            }
            
            Clock.schedule_once(lambda dt: self._on_connected(), 0)
            
        except Exception as e:
            Clock.schedule_once(
                lambda dt: self._on_connection_error(str(e)), 0
            )
    
    def _on_connected(self):
        """Called when successfully connected to server"""
        self.connected = True
        self.status_label.text = f'Status: Ready - Waiting for calls from {ALLOWED_CALLER}'
        
        # Start polling for incoming calls
        self.check_interval = Clock.schedule_interval(
            lambda dt: self.check_for_calls(), 3
        )
    
    def _on_connection_error(self, error):
        """Handle connection errors"""
        self.status_label.text = f'Connection Error: {error[:40]}'
        # Retry connection after 10 seconds
        Clock.schedule_once(lambda dt: self.auto_connect(), 10)
    
    def check_for_calls(self):
        """Poll server for incoming calls"""
        if not self.connected or self.in_call:
            return
        
        Thread(target=self._check_calls_thread).start()
    
    def _check_calls_thread(self):
        """Check for incoming calls in background thread"""
        try:
            # In production, this would be a proper endpoint
            # For now, simulate checking for calls
            time.sleep(0.5)
            
            # Simulate incoming call detection (in real app, server would notify)
            # For testing, you can uncomment the next line to simulate a call
            # Clock.schedule_once(lambda dt: self.auto_accept_call(ALLOWED_CALLER), 0)
            
        except Exception as e:
            pass
    
    def auto_accept_call(self, caller_id):
        """Automatically accept call from whitelisted caller"""
        if self.in_call:
            return
        
        if caller_id != ALLOWED_CALLER:
            self.status_label.text = f'Status: Rejected call from unauthorized device: {caller_id}'
            return
        
        self.in_call = True
        self.status_label.text = f'Status: Auto-accepting call from {caller_id}...'
        Thread(target=self._accept_call_thread, args=(caller_id,)).start()
    
    def _accept_call_thread(self, caller_id):
        """Accept the call in background"""
        try:
            # Prepare to accept call
            accept_data = {
                'receiver_id': DEVICE_ID,
                'caller_id': caller_id,
                'status': 'accepted'
            }
            
            time.sleep(1)
            
            Clock.schedule_once(lambda dt: self._on_call_accepted(caller_id), 0)
            
        except Exception as e:
            Clock.schedule_once(
                lambda dt: self._on_call_error(str(e)), 0
            )
    
    def _on_call_accepted(self, caller_id):
        """Called when call is successfully accepted"""
        self.status_label.text = f'Status: Call Active with {caller_id}'
        self.camera.play = True
        
        # In full implementation, start video streaming here
        # For now, just show that call is active
        
        # Schedule call end check
        Clock.schedule_once(lambda dt: self.check_call_status(), 5)
    
    def _on_call_error(self, error):
        """Handle call acceptance errors"""
        self.status_label.text = f'Call Error: {error[:40]}'
        self.in_call = False
    
    def check_call_status(self):
        """Check if call is still active"""
        if not self.in_call:
            return
        
        # In production, check with server if caller is still connected
        # For now, keep call active
        Clock.schedule_once(lambda dt: self.check_call_status(), 5)
    
    def end_call(self):
        """End the current call"""
        self.in_call = False
        self.camera.play = False
        self.status_label.text = f'Status: Ready - Waiting for calls from {ALLOWED_CALLER}'
    
    def on_stop(self):
        """Cleanup when app closes"""
        if self.check_interval:
            self.check_interval.cancel()
        self.camera.play = False
        return True

if __name__ == '__main__':
    ReceiverApp().run()
