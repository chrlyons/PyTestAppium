import pytest

from src.managers.appium_manager import AppiumManager
from src.managers.emulator_manager import EmulatorManager
from src.utils.driver_factory import DriverFactory
from src.utils.environment import EnvironmentSetup
from src.utils.logger import LoggerSetup

logger = LoggerSetup.setup_logger("mobile_testing")


@pytest.fixture(scope="session", autouse=True)
def setup_environment():
    """
    Session-wide test setup.
    - Sets environment variables
    - Ensures APK availability
    - Creates and starts emulator
    - Starts Appium server
    """
    # Setup
    EnvironmentSetup.setup_environment_variables()
    # Ensure APK is available but we don't need to store the path here
    EnvironmentSetup.ensure_apk_available()

    EmulatorManager.create_avd()
    if not EmulatorManager.start_emulator():
        pytest.exit("Emulator failed to start.")

    AppiumManager.start()

    # Setup
    yield
    # Teardown
    logger.info("Stopping Appium server and emulator...")
    AppiumManager.stop()
    EmulatorManager.stop_emulator()


@pytest.fixture
def driver():
    """
    Fixture that provides a configured Appium driver for tests.
    The driver is created before each test and quit afterward.
    """
    app_path = "apps/ApiDemos-debug.apk"
    driver = DriverFactory.create_android_driver(app_path)

    # Set implicit wait to ensure elements are found
    # driver.implicitly_wait(10)

    # Setup
    yield driver  # Test
    # Teardown

    # Always quit the driver after test completion
    driver.quit()
