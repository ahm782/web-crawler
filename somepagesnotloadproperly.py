import os
import time
import base64
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#  Pages to screenshot only
slow_pages = [ 
    8, 14, 32, 33, 46, 47, 48, 59, 50, 73, 74, 76, 79,
    92, 118, 120, 122, 124, 126, 129, 132, 134, 137, 139,
    144, 149, 151, 153, 155, 157, 162, 166, 168, 170, 172,
    174, 177, 180, 187, 193, 194, 239, 240, 258, 260
]

#  Output folder
os.makedirs("raw-data", exist_ok=True)

#  Browser config
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
options.add_argument("--disable-gpu")

# Launch Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#  Screenshot function
def fullpage_screenshot(driver, output_path):
    time.sleep(2)
    try:
        read_more = driver.find_element(By.CLASS_NAME, "toggle-detail")
        read_more.click()
        print(" 'Read more' clicked")
        time.sleep(1)
    except:
        print(" 'Read more' not found")

    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")

    driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
        "mobile": False,
        "width": width,
        "height": height,
        "deviceScaleFactor": 1
    })

    screenshot_data = driver.execute_cdp_cmd("Page.captureScreenshot", {"format": "png", "fromSurface": True})
    image_data = base64.b64decode(screenshot_data["data"])

    with open(output_path, "wb") as f:
        f.write(image_data)

    print(f" Saved: {output_path}")

#  Base site
base_url = "https://bilaunwan.pk/?page="

#  Go through each selected page
for page in slow_pages:
    print(f"\n Visiting: Page {page}")
    driver.get(base_url + str(page))
    time.sleep(10)
    save_path = f"raw-data/page_{page + 1}.png"
    fullpage_screenshot(driver, save_path)

#  Done
driver.quit()
print("\n All screenshots completed!")
