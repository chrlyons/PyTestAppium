# Mobile Testing Setup Guide

## Core Dependencies

### 1. Python Environment with Poetry
```bash
# Install project dependencies
poetry install

# Activate Poetry shell
poetry shell
```

### 2. Java Runtime Environment (JRE)
```bash
# Install Java using Homebrew
brew install --cask oracle-jdk

# Verify Java installation
java -version
```

### 3. Node.js and Appium
```bash
# Install Node.js
brew install node

# Install Appium
npm install -g appium

# Install Appium Driver
appium driver install uiautomator2
```

### 4. Android SDK Setup
1. Install Android Studio:
```bash
brew install --cask android-studio
```

2. Android SDK Components (through Android Studio):
   - Launch Android Studio
   - Click "More Actions" (or "Tools")
   - Select "SDK Manager"
   - In "SDK Tools" tab, check:
     - "Android SDK Command-line Tools"
     - "Android SDK Platform-Tools"
     - "Android Emulator"
   - Click "Apply" and wait for installation

3. Set Environment Variables:
   Add to `~/.zshrc`:
```bash
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/tools/bin
```

4. Apply changes:
```bash
source ~/.zshrc
```

5. Verify setup:
```bash
adb version
```

### 5. Test Application
```bash
# Create apps directory in project root
mkdir apps
cd apps

# Download API Demos APK
curl -L -o ApiDemos-debug.apk https://github.com/appium/appium/raw/master/packages/appium/sample-code/apps/ApiDemos-debug.apk
```

## Project Structure
```
mobile_testing/
├── pyproject.toml
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_app.py
└── apps/
    └── ApiDemos-debug.apk
```

## Running Tests
The test framework will automatically:
- Create and manage Android Virtual Devices
- Start/stop the emulator as needed
- Handle Appium server lifecycle
- Run the tests in the configured environment

Simply run:
```bash
pytest tests/
```

## Troubleshooting

### Common Issues

1. "Unable to locate a Java Runtime"
   - Install Java: `brew install --cask oracle-jdk`
   - Verify installation: `java -version`

2. "Android SDK cmdline-tools not found"
   - Open Android Studio → SDK Manager
   - Select "SDK Tools" tab
   - Check "Android SDK Command-line Tools"
   - Click "Apply"

3. "adb: command not found"
   - Verify environment variables in ~/.zshrc
   - Check if platform-tools is installed in SDK Manager

4. System Image Issues
   - Test framework will handle downloading and installing required system images
   - If you see permission issues, run Android Studio once to accept licenses

## Additional Resources
- [Java SE Downloads](https://www.oracle.com/java/technologies/downloads/)
- [Android Studio](https://developer.android.com/studio)
- [Appium Documentation](http://appium.io/docs/en/about-appium/getting-started/)