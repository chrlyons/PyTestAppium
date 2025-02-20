import os
import subprocess

from src.utils.logger import LoggerSetup

logger = LoggerSetup.get_logger("environment")


class EnvironmentSetup:
    """Utility class for environment setup operations"""

    @staticmethod
    def setup_environment_variables():
        """Set environment variables required for Android testing"""
        logger.info("Setting up environment variables for Android testing...")

        if "ANDROID_HOME" not in os.environ:
            os.environ["ANDROID_HOME"] = os.path.expanduser("~/Library/Android/sdk")
            logger.info(
                f"ANDROID_HOME not found, setting to {os.environ['ANDROID_HOME']}"
            )
        else:
            logger.info(f"Using existing ANDROID_HOME: {os.environ['ANDROID_HOME']}")

        if "ANDROID_SDK_ROOT" not in os.environ:
            os.environ["ANDROID_SDK_ROOT"] = os.environ["ANDROID_HOME"]
            logger.info(
                f"ANDROID_SDK_ROOT not found, setting to {os.environ['ANDROID_SDK_ROOT']}"
            )
        else:
            logger.info(
                f"Using existing ANDROID_SDK_ROOT: {os.environ['ANDROID_SDK_ROOT']}"
            )

        # Add necessary paths to PATH
        path_updates = [
            f"{os.environ['ANDROID_HOME']}/platform-tools",
            f"{os.environ['ANDROID_HOME']}/emulator",
            f"{os.environ['ANDROID_HOME']}/cmdline-tools/latest/bin",
        ]

        for path in path_updates:
            if path not in os.environ["PATH"]:
                os.environ["PATH"] += f":{path}"
                logger.info(f"Added to PATH: {path}")

        logger.debug(f"Final PATH: {os.environ['PATH']}")

    @staticmethod
    def ensure_apk_available(apk_path="apps/ApiDemos-debug.apk"):
        """Ensure the test APK is available at the specified path"""
        apk_path = os.path.abspath(apk_path)

        if not os.path.exists(apk_path):
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(apk_path), exist_ok=True)
            logger.info(f"Created directory: {os.path.dirname(apk_path)}")

            logger.info(f"APK not found at {apk_path}, downloading...")
            try:
                subprocess.run(
                    [
                        "curl",
                        "-L",
                        "-o",
                        apk_path,
                        "https://github.com/appium/appium/raw/master/packages/appium/sample-code/apps/ApiDemos-debug.apk",
                    ],
                    check=True,
                )
                logger.info(f"APK downloaded successfully to {apk_path}")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to download APK: {e}")
                raise
        else:
            logger.info(f"APK already exists at {apk_path}")

        # Verify file exists after download
        if not os.path.exists(apk_path):
            logger.error(f"APK still not found at {apk_path} after attempted download")
            raise FileNotFoundError(f"Could not find or download APK to {apk_path}")

        logger.info(
            f"APK ready at {apk_path} ({os.path.getsize(apk_path) / 1024:.1f} KB)"
        )
        return apk_path
