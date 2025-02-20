from appium.webdriver.common.appiumby import AppiumBy


def test_app_launch(driver):
    """Verify the API Demos app launches and interacts with UI"""
    # Act
    driver.implicitly_wait(10)

    # Arrange
    accessibility_button = driver.find_element(
        AppiumBy.XPATH, "//android.widget.TextView[@content-desc='Accessibility']"
    )
    accessibility_button.click()

    # Assert
    custom_view = driver.find_element(
        AppiumBy.XPATH, "//android.widget.TextView[@content-desc='Custom View']"
    )
    assert custom_view.is_displayed()
