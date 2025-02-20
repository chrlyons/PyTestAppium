import logging
import os
import socket
import subprocess
import time

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AVD_NAME = "test_device"
ANDROID_HOME = os.environ.get(
    "ANDROID_HOME", os.path.expanduser("~/Library/Android/sdk")
)
ADB_PATH = os.path.join(ANDROID_HOME, "platform-tools/adb")
EMULATOR_PATH = os.path.join(ANDROID_HOME, "emulator/emulator")
SDKMANAGER = os.path.join(ANDROID_HOME, "cmdline-tools/latest/bin/sdkmanager")
AVDMANAGER = os.path.join(ANDROID_HOME, "cmdline-tools/latest/bin/avdmanager")


class EmulatorManager:
    """Handles creation and startup of Android emulator"""

    @staticmethod
    def list_avds():
        """Return a list of existing AVDs"""
        try:
            result = subprocess.run(
                [EMULATOR_PATH, "-list-avds"], capture_output=True, text=True
            )
            return result.stdout.strip().split("\n")
        except FileNotFoundError:
            logger.error(
                f"Emulator binary not found at {EMULATOR_PATH}. Check your ANDROID_HOME setup."
            )
            return []

    @staticmethod
    def create_avd():
        """Create the AVD if it does not exist"""
        if AVD_NAME in EmulatorManager.list_avds():
            logger.info(f"AVD {AVD_NAME} already exists.")
            return

        logger.info(f"Creating AVD {AVD_NAME}...")
        try:
            subprocess.run(
                [SDKMANAGER, "system-images;android-30;google_apis;arm64-v8a"],
                check=True,
            )
            subprocess.run(
                [SDKMANAGER, "--licenses"], input="y\n" * 10, text=True, check=True
            )
            subprocess.run(
                [
                    AVDMANAGER,
                    "create",
                    "avd",
                    "-n",
                    AVD_NAME,
                    "-k",
                    "system-images;android-30;google_apis;arm64-v8a",
                    "-d",
                    "pixel",
                    "--force",
                ],
                check=True,
            )
            logger.info(f"AVD {AVD_NAME} created successfully.")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to create AVD: {e}")

    @staticmethod
    def start_emulator():
        """Start the emulator if it's not running"""
        if EmulatorManager.is_emulator_running():
            logger.info("Emulator is already running.")
            return True

        logger.info(f"Starting emulator: {AVD_NAME}")
        subprocess.Popen(
            [
                EMULATOR_PATH,
                "-avd",
                AVD_NAME,
                "-no-audio",
                "-no-window",
                "-gpu",
                "swiftshader_indirect",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        return EmulatorManager.wait_for_emulator()

    @staticmethod
    def wait_for_emulator(timeout=120):
        """Wait for emulator to be fully booted"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                result = subprocess.run(
                    [ADB_PATH, "shell", "getprop", "sys.boot_completed"],
                    capture_output=True,
                    text=True,
                )
                if result.stdout.strip() == "1":
                    logger.info("Emulator is fully booted.")
                    return True
                time.sleep(5)
            except Exception:
                time.sleep(5)
        logger.error("Emulator did not start within timeout.")
        return False

    @staticmethod
    def is_emulator_running():
        """Check if an emulator is currently running"""
        try:
            result = subprocess.run(
                [ADB_PATH, "devices"], capture_output=True, text=True
            )
            return "emulator" in result.stdout
        except FileNotFoundError:
            logger.error("ADB not found. Ensure Android SDK is properly installed.")
            return False

    @staticmethod
    def stop_emulator():
        """Stop the emulator"""
        try:
            subprocess.run([ADB_PATH, "emu", "kill"], check=False)
            logger.info("Emulator stopped.")
        except Exception:
            pass


class AppiumServer:
    """Manages Appium server"""

    process = None  # Store process reference

    @staticmethod
    def is_running():
        """Check if Appium server is running by connecting to its port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(("localhost", 4723))
            sock.close()
            return result == 0
        except Exception:
            return False

    @staticmethod
    def start():
        """Start Appium server if not already running"""
        if AppiumServer.is_running():
            logger.info("Appium server is already running.")
            return

        logger.info("Starting Appium server...")
        AppiumServer.process = subprocess.Popen(
            ["appium"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )

        # Wait for Appium to be fully initialized
        for _ in range(30):
            if AppiumServer.is_running():
                logger.info("Appium server started successfully.")
                return
            time.sleep(2)

        logger.error("Appium server failed to start.")

    @staticmethod
    def stop():
        """Stop Appium server"""
        if AppiumServer.process:
            AppiumServer.process.terminate()
            AppiumServer.process.wait(timeout=5)
            logger.info("Appium server stopped.")
        else:
            logger.info("No running Appium server to stop.")


@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    """Ensure the emulator and Appium server are running before tests"""

    # Set Environment Variables at runtime if not already set
    if "ANDROID_HOME" not in os.environ:
        os.environ["ANDROID_HOME"] = os.path.expanduser("~/Library/Android/sdk")
    if "ANDROID_SDK_ROOT" not in os.environ:
        os.environ["ANDROID_SDK_ROOT"] = os.environ["ANDROID_HOME"]

    os.environ["PATH"] += f":{os.environ['ANDROID_HOME']}/platform-tools"
    os.environ["PATH"] += f":{os.environ['ANDROID_HOME']}/emulator"
    os.environ["PATH"] += f":{os.environ['ANDROID_HOME']}/cmdline-tools/latest/bin"

    logger.info(f"ANDROID_HOME set to {os.environ['ANDROID_HOME']}")
    logger.info(f"PATH: {os.environ['PATH']}")

    # Ensure APK is available
    APK_PATH = os.path.abspath("apps/ApiDemos-debug.apk")
    if not os.path.exists(APK_PATH):
        logger.info("APK not found, downloading...")
        subprocess.run(
            [
                "curl",
                "-L",
                "-o",
                APK_PATH,
                "https://github.com/appium/appium/raw/master/packages/appium/sample-code/apps/ApiDemos-debug.apk",
            ],
            check=True,
        )

    # Ensure emulator and Appium server are running
    EmulatorManager.create_avd()
    if not EmulatorManager.start_emulator():
        pytest.exit("Emulator failed to start.")

    AppiumServer.start()

    # Setup
    yield  # Test
    # Teardown

    logger.info("Stopping Appium server and emulator...")
    AppiumServer.stop()
    EmulatorManager.stop_emulator()


@pytest.fixture
def driver():
    """Setup Appium driver for test session"""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "emulator-5554"
    options.app = os.path.abspath("apps/ApiDemos-debug.apk")

    driver = webdriver.Remote("http://localhost:4723", options=options)
    yield driver
    driver.quit()
