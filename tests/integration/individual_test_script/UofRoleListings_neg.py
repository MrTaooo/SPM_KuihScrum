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
# ensure that 'hr' is clicked
staff = driver.find_element(By.ID, "hr")
staff.click()



# find all job listings 
try:
    # Find multiple elements by class name
    elements = driver.find_elements(By.CSS_SELECTOR,".job_listing")
    rolename = elements[0].find_element(By.CLASS_NAME, "card-title")
    # search for edit button
    edit = elements[0].find_element(By.CLASS_NAME, "edit_btn")
    edit.click() 
    time.sleep(1)
    date_input = driver.find_element(By.ID, "editClosingDate")
    
    # enter date
    year = "2023"
    month = "12"
    day = "15"
    # Format the date in "mm/dd/yyyy" format
    formatted_date = f"{month}/{day}/{year}"

    # Clear the existing value in the input field
    date_input.clear()  
    # Send the formatted date string
    date_input.send_keys(formatted_date)  
    time.sleep(1)

    save_button = driver.find_element(By.ID, "editButton")
    save_button.click() 
    time.sleep(1)
    
except NoSuchElementException:
    print("Test Case Failed")



# check conditions
error = driver.find_element(By.ID, "editErrorMessage")
if error.text == "Error, cannot have duplicate listings":
    print("Test case Successful!")
else:
    print("Error message not found. Test case Failed.")


print("End of Test Case")

