[app]

# (str) Title of your application
title = Galaxy

# (str) Package name
package.name = galaxygame

# (str) Package domain (needed for android/ios packaging)
package.domain = org.galaxy

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,kv,json,ttf,wav,mp3,png,jpg

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts =

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = .venv,__pycache__,.git,.github,screenshot,build,dist,wheels

# (str) Application versioning
version = 0.1.0

# (list) Application requirements
requirements = python3,kivy

# (str) Presplash of the application (a loading screen image)
#presplash.filename = %(source.dir)s/assets/images/bg1.jpg

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (landscape, sensorLandscape, portrait, sensorPortrait, all)
orientation = landscape

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

#
# Android specific
#

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK / AAB will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (list) The Android archs to build for
android.archs = arm64-v8a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (bool) If True, then skip trying to update the Android sdk
# android.skip_update = False

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) The format used to package the app for release mode (aab or apk or aar).
android.release_artifact = apk

# (str) The format used to package the app for debug mode (apk or aar).
android.debug_artifact = apk

#
# Python for android (p4a) specific
#

# (str) python-for-android URL to use for checkout
#p4a.source_dir =

# (str) The directory in which python-for-android should look for your own build recipes (if any)
#p4a.local_recipes =

# (str) Filename to the hook for p4a
#p4a.hook =

# (str) Bootstrap to use for android builds
p4a.bootstrap = sdl2

#
# iOS specific (not used for this project)
#

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
