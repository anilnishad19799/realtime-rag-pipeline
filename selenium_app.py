# selenium_app.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, os

URL = os.getenv("DASHBOARD_URL", "http://localhost:8000")
PDF_PATH = os.getenv("PDF_PATH", "sample.pdf")

def run_selenium_dashboard():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    time.sleep(2)

    # upload file
    file_input = driver.find_element(By.ID, "pdfFile")
    file_input.send_keys(os.path.abspath(PDF_PATH))
    submit_btn = driver.find_element(By.XPATH, "//button[text()='Upload']")
    submit_btn.click()
    print("PDF uploaded, watching dashboard...")

    # keep browser open to observe progress
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        driver.quit()

if __name__ == "__main__":
    run_selenium_dashboard()
