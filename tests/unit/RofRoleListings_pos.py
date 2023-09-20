# import webdriver
from selenium import webdriver
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# create webdriver object
driver = webdriver.Chrome()
# get url
driver.get("http://127.0.0.1:5500/templates/index.html")
time.sleep(1)
# ensure that 'hr' is clicked
staff = driver.find_element(By.ID, "hr")
staff.click()

# find create new role listing button
element = driver.find_element(By.XPATH, "//button[@class='btn btn-dark']")
actual_name = element.text
expected_name = "Create a Job Listing"

# assert actual_title == expected_title
assert expected_name in actual_name, f"Expected title: '{expected_name}', Actual title: '{actual_name}'"
print("Test case passed!")
time.sleep(1)

