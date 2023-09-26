# import webdriver
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
roleTitle = "Software Developer"
dropdown.select_by_visible_text(roleTitle)

# enter date
year = "2023"
month = "09"
day = "27"
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

# wait for modal to appear
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.ID, "closeModal")))

# close modal
close = driver.find_element(By.ID, "closeModal")
close.click()

expected_closing_dates[roleTitle] = date # add to dictionary

# find all job title and closing dates
job_title_elements = driver.find_elements(By.CSS_SELECTOR, ".card-title.m-2")
closing_date_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'text-center')]/h5[contains(text(), 'Closing Date:')]")

# job titles and closing date elements
if job_title_elements and closing_date_elements:
    # latest job title and closing date
    latest_job_title = job_title_elements[-1].text
    latest_closing_date_element = closing_date_elements[-1]
    latest_closing_date_text = latest_closing_date_element.text.split(":")[1].strip()

    # check if the latest closing date matches the expected date
    if latest_job_title in expected_closing_dates:
        expected_date = expected_closing_dates[latest_job_title]
        if latest_closing_date_text == expected_date:
            print(f"Latest Job Title: {latest_job_title}, Closing Date: {latest_closing_date_text} (Correct)")
        else:
            print(f"Latest Job Title: {latest_job_title}, Closing Date: {latest_closing_date_text} (Incorrect)")
    else:
        print(f"Latest Job Title: {latest_job_title} (No Expected Closing Date Found)")
else:
    print("No job titles or closing dates found.")

print("Test case finished!")

