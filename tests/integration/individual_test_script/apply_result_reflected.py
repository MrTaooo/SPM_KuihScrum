# import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# create webdriver object
# Define ChromeOptions to run headless
chrome_options = webdriver.ChromeOptions()
# headless means that the browser will not open up
# chrome_options.add_argument("--headless")

# Use ChromeDriverManager to download and manage ChromeDriver
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# get url
driver.get("http://127.0.0.1:5500/templates/index.html")

hr = driver.find_element(By.ID, "hr")
hr.click()
time.sleep(1)

try: 
    # comparison data for staff with ID 1 who applied for Data Analyst job listing in automated test case 5 
    num_skill_matched = 1
    num_role_skill = 3
    job_list_name = 'Data Analyst'


    job_listings = driver.find_elements_by_css_selector(".job_listing")
    for listing in job_listings:
        job_title = listing.find_element(By.CLASS_NAME, 'card-title').text
        if job_list_name == job_title: 
            progress_bar = listing.find_element(By.CLASS_NAME, 'progress-bar')
            progress_bar_text = progress_bar.text.replace('%', '')
            if str(round(num_skill_matched/num_role_skill*100)) == progress_bar_text:
                print('Test Case Successful!')


except Exception as e:
    print(f"An error occurred: {e.message}")

finally:
    driver.quit()