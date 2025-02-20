from appium.webdriver.common.appiumby import AppiumBy


def test_app_launch(driver):
    """Verify the API Demos app launches and interacts with UI"""
    # Wait for app to load
    driver.implicitly_wait(10)

    # Locate the 'Accessibility' button and click it
    accessibility_button = driver.find_element(
        AppiumBy.XPATH, "//android.widget.TextView[@content-desc='Accessibility']"
    )
    accessibility_button.click()

    # Verify that a new screen opens
    custom_view = driver.find_element(
        AppiumBy.XPATH, "//android.widget.TextView[@content-desc='Custom View']"
    )
    assert custom_view.is_displayed()
