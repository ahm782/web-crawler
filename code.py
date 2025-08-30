import os
import time
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Create folder
os.makedirs("raw-data", exist_ok=True)

# Chrome options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def fullpage_screenshot(driver, output_path):
    time.sleep(2)

    # Click 'Read more' if present
    try:
        read_more = driver.find_element(By.CLASS_NAME, "toggle-detail")
        read_more.click()
        print("'Read more' clicked")
        time.sleep(1)
    except:
        print(" 'Read more' not found")

    # Get full width and height using JavaScript (to avoid width crop)
    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")

    # Override device size
    driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
        "mobile": False,
        "width": width,
        "height": height,
        "deviceScaleFactor": 1
    })

    # Capture screenshot
    screenshot_data = driver.execute_cdp_cmd("Page.captureScreenshot", {"format": "png", "fromSurface": True})
    image_data = base64.b64decode(screenshot_data["data"])

    with open(output_path, "wb") as f:
        f.write(image_data)

    print(f" Saved: {output_path}")

# Visit page
driver.get("https://bilaunwan.pk")
print(" Visiting: https://bilaunwan.pk")
time.sleep(3)

# Loop through all pages (266)
for i in range(1, 267):
    print(f"\n Capturing Page {i}")
    fullpage_screenshot(driver, f"raw-data/page_{i}.png")

    # Click next
    try:
        next_btn = driver.find_element(By.CLASS_NAME, "next-btn")
        driver.execute_script("arguments[0].scrollIntoView();", next_btn)
        next_btn.click()
        print(" Clicked next")
        time.sleep(3)
    except:
        print(" No next button found. Stopping.")
        break

driver.quit()
