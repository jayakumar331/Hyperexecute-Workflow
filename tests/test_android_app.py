from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PKG = "com.lambdatest.proverbial:id/"
TIMEOUT = 20


def _id(name):
    return (AppiumBy.ID, PKG + name)


def _a11y(name):
    return (AppiumBy.ACCESSIBILITY_ID, name)


def tap(driver, locator):
    WebDriverWait(driver, TIMEOUT).until(EC.element_to_be_clickable(locator)).click()


def wait_visible(driver, locator):
    return WebDriverWait(driver, TIMEOUT).until(EC.visibility_of_element_located(locator))


def test_proverbial_app_flow(driver):
    # Color toggles to pink and back
    tap(driver, _id("color"))
    tap(driver, _id("color"))

    # Text changes to "Proverbial"
    tap(driver, _id("Text"))

    # Toast and notification
    tap(driver, _id("toast"))
    tap(driver, _id("notification"))

    # Geolocation page, then back home
    tap(driver, _id("geoLocation"))
    tap(driver, _a11y("Home"))

    # Speed test page, then back home
    tap(driver, _id("speedTest"))
    tap(driver, _a11y("Home"))

    # In-app browser: load a URL through the tunnel
    tap(driver, _a11y("Browser"))
    url = wait_visible(driver, _id("url"))
    url.send_keys("https://www.lambdatest.com")
    tap(driver, _id("find"))
