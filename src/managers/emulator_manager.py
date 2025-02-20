import os
import subprocess
import time

from src.utils.logger import LoggerSetup

logger = LoggerSetup.get_logger("emulator")

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
        except Exception as e:
            logger.error(f"Error stopping emulator: {e}")
