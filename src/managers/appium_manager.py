import socket
import subprocess
import time

from src.utils.logger import LoggerSetup

logger = LoggerSetup.get_logger("appium")


class AppiumManager:
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
        except Exception as e:
            logger.error(f"Error checking if Appium is running: {e}")
            return False

    @staticmethod
    def start():
        """Start Appium server if not already running"""
        if AppiumManager.is_running():
            logger.info("Appium server is already running.")
            return

        logger.info("Starting Appium server...")
        try:
            AppiumManager.process = subprocess.Popen(
                ["appium"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
            )

            # Wait for Appium to be fully initialized
            for i in range(30):
                if AppiumManager.is_running():
                    logger.info("Appium server started successfully.")
                    return
                logger.debug(
                    f"Waiting for Appium server to start (attempt {i+1}/30)..."
                )
                time.sleep(2)

            logger.error("Appium server failed to start after timeout.")
        except Exception as e:
            logger.error(f"Error starting Appium server: {e}")

    @staticmethod
    def stop():
        """Stop Appium server"""
        if AppiumManager.process:
            try:
                AppiumManager.process.terminate()
                AppiumManager.process.wait(timeout=5)
                logger.info("Appium server stopped.")
            except Exception as e:
                logger.error(f"Error stopping Appium server: {e}")
                # Force kill if terminate fails
                try:
                    AppiumManager.process.kill()
                    logger.info("Appium server force killed.")
                except Exception as e2:
                    logger.error(f"Failed to force kill Appium server: {e2}")
        else:
            logger.info("No running Appium server to stop.")
