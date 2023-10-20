# import webdriver
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

import time

# create webdriver object
driver = webdriver.Chrome()
# get url
driver.get("http://127.0.0.1:5500/templates/index.html")
time.sleep(1)
expected_closing_dates = {}
# ensure that 'hr' is clicked
staff = driver.find_element(By.ID, "hr")
staff.click()
time.sleep(1)

# find create new role listing button and create a new role listing
element = driver.find_element(By.XPATH, "//button[@class='btn btn-dark']")
element.click()
time.sleep(1)
dropdown = Select(driver.find_element(By.ID, "roleTitle")) 
roleTitle = "Sales Representative"
dropdown.select_by_visible_text(roleTitle)

# enter date
year = "2023"
month = "10"
day = "09"
date = f"{year}-{month}-{day}"
date_input = driver.find_element(By.ID, "closingDate")
date_input.click()
date_input.send_keys(year)
date_input.send_keys(Keys.LEFT)
date_input.send_keys(month)
date_input.send_keys(Keys.LEFT)
date_input.send_keys(Keys.LEFT)
date_input.send_keys(day)
date_input.send_keys(Keys.RETURN)
time.sleep(1)

# save job listing
submit = driver.find_element(By.ID, "jobCreationButton")
submit.click()
time.sleep(3)

try:
    error = driver.find_element(By.ID, "errorMessage")
    if error.text == "Error, cannot have duplicate listings":
        print("Test case Successful!")
    else:
        print("Error message not found. Test case Failed.")

finally:
    driver.quit()
