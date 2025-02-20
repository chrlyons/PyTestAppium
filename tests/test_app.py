from appium.webdriver.common.appiumby import AppiumBy

from src.utils.logger import LoggerSetup

logger = LoggerSetup.get_logger("test")


def test_app_launch(driver):
    """Verify the API Demos app launches and interacts with UI"""
    logger.info("Starting API Demos app launch test")

    # Arrange & Act - Find and click on the Accessibility button
    logger.info("Looking for Accessibility button")
    accessibility_button = driver.find_element(
        AppiumBy.XPATH, "//android.widget.TextView[@content-desc='Accessibility']"
    )
    logger.info("Clicking Accessibility button")
    accessibility_button.click()

    # Assert - Verify the Custom View element is displayed
    logger.info("Verifying Custom View element is displayed")
    custom_view = driver.find_element(
        AppiumBy.XPATH, "//android.widget.TextView[@content-desc='Custom View']"
    )
    is_displayed = custom_view.is_displayed()
    logger.info(f"Custom View element displayed: {is_displayed}")
    assert is_displayed, "Custom View element not displayed"

    logger.info("Test completed successfully")
