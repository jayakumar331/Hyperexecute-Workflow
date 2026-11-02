import os

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

LT_USERNAME = os.getenv("LT_USERNAME")
LT_ACCESS_KEY = os.getenv("LT_ACCESS_KEY")
GRID_URL = "mobile-hub.lambdatest.com/wd/hub"

APP_ID = os.getenv("LT_APP_ID", "lt://APP1016047701790175924963231")
# Regex patterns let LambdaTest allocate any free matching real device
DEVICE_NAME = os.getenv("DEVICE_NAME", "Galaxy.*")
PLATFORM_VERSION = os.getenv("PLATFORM_VERSION", "1[1-5]")
# LT_TUNNEL=true (set by the tunnel YAML) routes the session through the
# tunnel HyperExecute starts for the job.
TUNNEL = os.getenv("LT_TUNNEL", "false").lower() == "true"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        item.rep_call = report


@pytest.fixture
def driver(request):
    if not LT_USERNAME or not LT_ACCESS_KEY:
        pytest.fail("Set LT_USERNAME and LT_ACCESS_KEY environment variables")

    lt_options = {
        "w3c": True,
        "platformName": "android",
        "deviceName": DEVICE_NAME,
        "platformVersion": PLATFORM_VERSION,
        "isRealMobile": True,
        "app": APP_ID,
        "build": "Python Pytest Android - HyperExecute",
        "name": request.node.name,
        "deviceOrientation": "PORTRAIT",
        "console": True,
        "devicelog": True,
        "network": False,
        "autoGrantPermissions": True,
    }
    if TUNNEL:
        lt_options["tunnel"] = True

    options = UiAutomator2Options()
    options.set_capability("platformName", "android")
    options.set_capability("lt:options", lt_options)

    hub = f"https://{LT_USERNAME}:{LT_ACCESS_KEY}@{GRID_URL}"
    drv = webdriver.Remote(hub, options=options)
    drv.implicitly_wait(0)  # rely on explicit waits only

    yield drv

    # Mark the session result on the LambdaTest dashboard
    rep = getattr(request.node, "rep_call", None)
    status = "passed" if rep is not None and rep.passed else "failed"
    try:
        drv.execute_script(f"lambda-status={status}")
    finally:
        drv.quit()
