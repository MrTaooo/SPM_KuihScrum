# import webdriver
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time
from datetime import datetime

# create webdriver object
# Define ChromeOptions to run headless
chrome_options = webdriver.ChromeOptions()
# headless means that the browser will not open up
# chrome_options.add_argument("--headless")

# Use ChromeDriverManager to download and manage ChromeDriver
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# get url
driver.get("http://127.0.0.1:5500/templates/index.html")
time.sleep(1)
# expected_closing_dates = {}
# ensure that 'hr' is clicked
staff = driver.find_element(By.ID, "hr")
staff.click()
time.sleep(1)

# find create new role listing button and create a new role listing
element = driver.find_element(By.ID, "create_listing_btn")
element.click()
time.sleep(5)
dropdown = Select(driver.find_element(By.ID, "roleTitle")) 
roleTitle = "Sales Representative"
dropdown.select_by_visible_text(roleTitle)

# enter date
year = "2023"
month = "12"
day = "25"
# Format the date in "mm/dd/yyyy" format
formatted_date = f"{month}/{day}/{year}"

# Locate the date input field and enter the formatted date
date_input = driver.find_element(By.ID, "closingDate")
# Clear the existing value in the input field
date_input.clear()  
# Send the formatted date string
date_input.send_keys(formatted_date)  
time.sleep(1)

# save job listing
submit = driver.find_element(By.ID, "jobCreationButton")
submit.click()
time.sleep(1)

# check if job listing alr created after running the test script once
# first run of the day should be successful entry
# subsequent runs of the day should be unsuccessful entry (duplicate entry)
create_err_msg = driver.find_element(By.ID, "errorMessage").text
if create_err_msg:
    print("Test case failed: Duplicate entry")
    print("End of test case 3")
else:
    # Wait for the top modal to be visible
    top_modal = driver.find_element(By.ID, "successModal")

    # Locate the close button within the top modal
    close_button = top_modal.find_element(By.ID, "closeModal")

    # Click the close button to close the top modal
    close_button.click()


    # get the parent element of the job listing
    job_list_parent_element = driver.find_element_by_id('joblist_parent')

    # get the first child element of the job listing (aka first listing)
    first_job_listing = job_list_parent_element.find_element_by_css_selector('*:first-child')

    # Find the elements for role name, publish date, and closing date within the div
    role_name_element = first_job_listing.find_element_by_css_selector('.card-title')
    publish_date_element = first_job_listing.find_element_by_xpath(".//h5[contains(text(), 'Date Posted:')]")
    closing_date_element = first_job_listing.find_element_by_xpath(".//h5[contains(text(), 'Closing Date:')]")

    # Extract text from the elements
    role_name = role_name_element.text
    publish_date = publish_date_element.text.replace('Date Posted:', '').strip()
    closing_date = closing_date_element.text.replace('Closing Date:', '').strip()

    # get today's date
    today = time.strftime("%Y-%m-%d")

    # format date used above for "formatted_date" variable
    # Convert the input string to a datetime object
    input_date = datetime.strptime(formatted_date, "%m/%d/%Y")
    # Format the datetime object as "%y-%m-%d"
    formatted_date_string = input_date.strftime("%Y-%m-%d")

    # Check if first job list is the same as the one created (role name, publish date and closing date must match)
    if role_name == roleTitle and publish_date == today and closing_date == formatted_date_string:
        print("Test case passed: Job listing created successfully")
    else:
        print("Test case failed: Job listing not created successfully.")

    # expected_closing_dates[roleTitle] = formatted_date # add to dictionary

    # # find all job title and closing dates
    # job_title_elements = driver.find_elements(By.CSS_SELECTOR, ".card-title.m-2")
    # closing_date_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'text-center')]/h5[contains(text(), 'Closing Date:')]")

    # # job titles and closing date elements
    # if job_title_elements and closing_date_elements:
    #     # latest job title and closing date
    #     latest_job_title = job_title_elements[-1].text
    #     latest_closing_date_element = closing_date_elements[-1]
    #     latest_closing_date_text = latest_closing_date_element.text.split(":")[1].strip()

    #     # check if the latest closing date matches the expected date
    #     if latest_job_title in expected_closing_dates:
    #         expected_date = expected_closing_dates[latest_job_title]
    #         if latest_closing_date_text == expected_date:
    #             print(f"Latest Job Title: {latest_job_title}, Closing Date: {latest_closing_date_text} (Correct)")
    #         else:
    #             print(f"Latest Job Title: {latest_job_title}, Closing Date: {latest_closing_date_text} (Incorrect)")
    #     else:
    #         print(f"Latest Job Title: {latest_job_title} (No Expected Closing Date Found)")
    # else:
    #     print("No job titles or closing dates found.")

    print("End of test case 3")


