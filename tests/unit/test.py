# import webdriver
from selenium import webdriver
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# create webdriver object
driver = webdriver.Chrome()
# get url
driver.get("http://127.0.0.1:5500/templates/index.html")

element = driver.find_element(By.XPATH, "//a[@class='navbar-brand text-white']")
actual_title = element.text
expected_title = "All in One"

# assert actual_title == expected_title
assert expected_title in actual_title, f"Expected title: '{expected_title}', Actual title: '{actual_title}'"
print("Test case passed!")
time.sleep(5)

