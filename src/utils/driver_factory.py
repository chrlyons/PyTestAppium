import os

from appium import webdriver
from appium.options.android import UiAutomator2Options

from src.utils.logger import LoggerSetup

logger = LoggerSetup.get_logger("driver")


class DriverFactory:
    """Factory for creating Appium driver instances"""

    @staticmethod
    def create_android_driver(app_path=None, device_name="emulator-5554"):
        """
        Create and configure an Android driver

        Args:
            app_path: Path to the app under test
            device_name: Name of the device to connect to

        Returns:
            An initialized Appium driver
        """
        logger.info(f"Creating Android driver for device: {device_name}")

        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.automation_name = "UiAutomator2"
        options.device_name = device_name

        if app_path:
            abs_app_path = os.path.abspath(app_path)
            if os.path.exists(abs_app_path):
                options.app = abs_app_path
                logger.info(f"Using app at path: {abs_app_path}")
            else:
                logger.warning(f"App not found at path: {abs_app_path}")

        logger.debug(f"Driver options: {options.capabilities}")

        try:
            driver = webdriver.Remote("http://localhost:4723", options=options)
            logger.info("Appium driver created successfully")
            return driver
        except Exception as e:
            logger.error(f"Failed to create Appium driver: {e}")
            raise
