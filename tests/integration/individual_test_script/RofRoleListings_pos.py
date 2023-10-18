# import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

import time

# create webdriver object
# Define ChromeOptions to run headless
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")

# Use ChromeDriverManager to download and manage ChromeDriver
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# get url
driver.get("http://127.0.0.1:5500/templates/index.html")
time.sleep(1)
# ensure that 'hr' is clicked
staff = driver.find_element(By.ID, "hr")
staff.click()

# find create new role listing button
element = driver.find_element(By.ID, "create_listing_btn")
actual_create_name = element.text
expected_create_name = "Create a Job Listing"

# check for job listings
try:
    # Find multiple elements by class name
    elements = driver.find_elements_by_css_selector(".job_listing")
    # Get the number of elements
    number_of_elements = len(elements)
except NoSuchElementException:
    print("Test Case Failed")

# search for edit button
edit = driver.find_element_by_css_selector(".edit_btn")
actual_edit_name = edit.text
expected_edit_name = "Edit"

# check conditions
if (actual_create_name == expected_create_name) and (number_of_elements == 5) and (actual_edit_name == expected_edit_name):
    print("Test case passed!")
else:
    print("Test case failed.")

print("End of Test Case")

