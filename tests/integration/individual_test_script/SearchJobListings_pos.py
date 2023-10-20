# import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

import time

# create webdriver object
# Define ChromeOptions to run headless
options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")

# Use ChromeDriverManager to download and manage ChromeDriver
driver = webdriver.Chrome(options=options)
# get url
driver.get("http://127.0.0.1:5500/templates/index.html")
time.sleep(1)


# find all job listings 
try:
    # Find search bar 
    search_bar = driver.find_element(By.ID, "searchInput")
    search_bar.clear()
    search_bar.send_keys("account manager")
    time.sleep(1)
    # Find multiple elements by class name
    elements = driver.find_elements(By.CSS_SELECTOR,".job_listing")
    # Check each element's role name
    all_account_managers = True

    for element in elements:
        rolename = element.find_element(By.CLASS_NAME, "card-title").text.lower()
        time.sleep(1)
        if rolename != "account manager":
            all_account_managers = False
            break
except NoSuchElementException:
    print("Test Case Failed")


# Check conditions
if all_account_managers:
    print("Test case passed!")
else:
    print("Test case failed.")

print("End of Test Case")

