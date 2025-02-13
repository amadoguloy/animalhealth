from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json
import time
import os

# Set up Selenium WebDriver for GitHub Codespaces
options = Options()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--remote-debugging-port=9222")
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")
options.binary_location = "/usr/bin/google-chrome-stable"

service = Service("/usr/bin/chromedriver")  # Use system-installed ChromeDriver
browser = webdriver.Chrome(service=service, options=options)

url = "https://wahis.woah.org/#/dashboards/qd-dashboard"
browser.get(url)
time.sleep(10)  # Allow time for page to load

# Example: Extracting table data (Modify based on the actual site structure)
data = []
table_xpath = "//table[contains(@class, 'table-class')]"  # Update with the actual class or identifier

try:
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, table_xpath)))
    rows = browser.find_elements(By.XPATH, f"{table_xpath}/tbody/tr")
    
    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        data.append([col.text for col in cols])
    
    # Convert to DataFrame
    df = pd.DataFrame(data, columns=["Column1", "Column2", "Column3"])  # Update column names
    
    # Save as CSV
    csv_output_path = os.path.join(os.getenv("GITHUB_WORKSPACE", ""), "animal-health.csv")
    df.to_csv(csv_output_path, index=False)
    print(f"Data saved to {csv_output_path}")
    
    # Save as JSON
    json_output_path = os.path.join(os.getenv("GITHUB_WORKSPACE", ""), "animal-health.json")
    df.to_json(json_output_path, orient="records", indent=4)
    print(f"Data saved to {json_output_path}")
    
except Exception as e:
    print("Error extracting data:", e)

browser.quit()
