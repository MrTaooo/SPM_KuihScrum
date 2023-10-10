# import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import time

# create webdriver object
# Define ChromeOptions to run headless
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")

# Use ChromeDriverManager to download and manage ChromeDriver
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# get url
driver.get("http://127.0.0.1:5500/templates/index.html")

# ensure that 'staff' is clicked
staff = driver.find_element(By.ID, "staff")
staff.click()

# check for job listings
try:
    # Find multiple elements by class name
    elements = driver.find_elements_by_css_selector(".job_listing")
    # Get the number of elements
    number_of_elements = len(elements)
    # based on the test.sql, there should only be 2 job listings shown if a staff logs in
    if (number_of_elements == 2):
        print("Test Case Passed: Job Listings Found and number of Job Listings matches expected number")
except NoSuchElementException:
    print("Test Case Failed")

print("End of Test Case")

