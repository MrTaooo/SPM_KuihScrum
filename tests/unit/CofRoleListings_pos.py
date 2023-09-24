# import webdriver
from selenium import webdriver
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

# create webdriver object
driver = webdriver.Chrome()
# get url
driver.get("http://127.0.0.1:5500/templates/index.html")
time.sleep(1)
# ensure that 'hr' is clicked
staff = driver.find_element(By.ID, "hr")
staff.click()
time.sleep(1)

# find create new role listing button and create a new role listing
element = driver.find_element(By.XPATH, "//button[@class='btn btn-dark']")
# actual_name = element.text
# expected_name = "Create a Job Listing"
element.click()
time.sleep(1)
dropdown = Select(driver.find_element(By.ID, "roleTitle")) 
roleTitle = "Data Analyst"
dropdown.select_by_visible_text(roleTitle)

# Locate the input field that opens the date picker and enter in a date
date_input = driver.find_element(By.ID, "closingDate")
date_input.click()
date_input.send_keys("2023")
date_input.send_keys(Keys.LEFT)
date_input.send_keys("09")
date_input.send_keys(Keys.LEFT)
date_input.send_keys(Keys.LEFT)
date_input.send_keys("26")
date_input.send_keys(Keys.RETURN)
time.sleep(1)

# save job listing
submit = driver.find_element(By.ID, "jobCreationButton")
submit.click()
time.sleep(1)

# close modal
close = driver.find_element(By.XPATH, "//button[@class='btn btn-secondary']")
close.click()

print("Test case passed!")

