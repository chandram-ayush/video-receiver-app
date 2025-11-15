[app]
title = VideoReceiver
package.name = videoreceiver
package.domain = org.autopick
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
source.main = main.py

# Minimal working requirements
requirements = python3,kivy,pillow,requests

# Permissions for receiver
android.permissions = INTERNET,CAMERA,RECORD_AUDIO,ACCESS_NETWORK_STATE,WAKE_LOCK

# Android settings
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

# Keep screen on during calls
android.wakelock = True

# Display
orientation = portrait
fullscreen = 0

# Background service (keeps app running)
android.presplash_color = #000000
android.icon = icon.png

[buildozer]
log_level = 2
warn_on_root = 1
