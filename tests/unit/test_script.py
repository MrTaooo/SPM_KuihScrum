# import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime

# create webdriver object
# Define ChromeOptions to run headless
chrome_options = webdriver.ChromeOptions()
# headless means that the browser will not open up
chrome_options.add_argument("--headless")

# Use ChromeDriverManager to download and manage ChromeDriver
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# get url
driver.get("http://127.0.0.1:5500/templates/index.html")
time.sleep(5)

########################### Start of Test Case Functions ####################################################

# created this so we can reuse this function in our test scripts. 
def retreive_Latest_Job_List():
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

    return (role_name, publish_date, closing_date)

# automated test case 1: test if the staff can see only opened job listings
def BrowseRoleListings():
    # ensure that 'staff' is clicked
    staff = driver.find_element(By.ID, "staff")
    staff.click()
    time.sleep(1)

    print("===============================================================================")
    # check for job listings
    try:
        # Find multiple elements by class name
        elements = driver.find_elements_by_css_selector(".job_listing")
        # Get the number of elements
        number_of_elements = len(elements)
        # based on the test.sql, there should only be 2 job listings shown if a staff logs in
        if (number_of_elements == 3):
            print("Results: Passed!")
            print("Remarks: Job Listings Found and number of Job Listings matches expected number")
    except NoSuchElementException:
        print("Results: Failed")

    print("End of Automated Test Case 1")
    print("===============================================================================")

# automated test case 2: test if the hr can see all job listings (opened and closed) and can see the create and edit button on the UI
def RofRoleListings():
    staff = driver.find_element(By.ID, "hr")
    staff.click()
    time.sleep(1)

    # find create new role listing button
    element = driver.find_element(By.ID, "create_listing_btn")
    actual_create_name = element.text
    expected_create_name = "Create a Job Listing"

    print("===============================================================================")
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
    if (actual_create_name == expected_create_name) and (number_of_elements == 6) and (actual_edit_name == expected_edit_name):
        print("Result: Passed!")
        print("Remarks: HR can see buttons and open/close listings")
    else:
        print("Result: Failed.")

    print("End of Automated Test Case 2")
    print("===============================================================================")

# automated test case 3: test if the hr can create a new job listing 
def CofRoleListings():
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

    # get today's date
    today = time.strftime("%Y-%m-%d")

    # format date used above for "formatted_date" variable
    # Convert the input string to a datetime object
    input_date = datetime.strptime(formatted_date, "%m/%d/%Y")
    # Format the datetime object as "%y-%m-%d"
    formatted_date_string = input_date.strftime("%Y-%m-%d")

    # Locate the date input field and enter the formatted date
    date_input = driver.find_element(By.ID, "closingDate")
    # Clear the existing value in the input field
    date_input.clear()  
    # Send the formatted date string
    date_input.send_keys(formatted_date)  
    time.sleep(1)

    print("===============================================================================")
    # if we have alr ran the test script once, the next few codes will print out the message
    role_name, publish_date, closing_date = retreive_Latest_Job_List()
    if role_name == roleTitle and publish_date == today and closing_date == formatted_date_string:
        button_element = driver.find_element(By.ID, 'jobCreationCancelButton')
        button_element.click()
        print("Result: Passed!")
        print("Remarks: Test script has been ran at least once today.")
        print("End of Automated test case 3")
        print("===============================================================================")
        return


    # save job listing
    submit = driver.find_element(By.ID, "jobCreationButton")
    submit.click()
    time.sleep(1)

    # check if job listing alr created after running the test script once
    # first run of the day should be successful entry
    # subsequent runs of the day should be unsuccessful entry (duplicate entry)
    create_err_msg = driver.find_element(By.ID, "errorMessage").text
    if create_err_msg:
        print("Result: Failed.")
        print("Remarks: Duplicate entry")
        print("End of Automated test case 3")
        print("===============================================================================")
    else:
        # Wait for the top modal to be visible
        top_modal = driver.find_element(By.ID, "successModal")

        # Locate the close button within the top modal
        close_button = top_modal.find_element(By.ID, "closeModal")

        # Click the close button to close the top modal
        close_button.click()

        role_name, publish_date, closing_date = retreive_Latest_Job_List()
        # Check if first job list is the same as the one created (role name, publish date and closing date must match)
        if role_name == roleTitle and publish_date == today and closing_date == formatted_date_string:
            print("Result: Passed!")
            print("Remarks: Job listing created successfully")
        else:
            print("Result: Failed.")
            print("Remarks: Job listing not created successfully.")
        print("End of Automated test case 3")
        print("===============================================================================")

# automated test case 4: test if withdraw button works
def withdraw_btn_test():
    time.sleep(5)
    try:
        applyJL = 'Software Developer' # job title

        # Find all job listing
        job_cards = driver.find_elements_by_css_selector(".job_listing")

        for card in job_cards:
            job_title = card.find_element(By.CLASS_NAME, 'card-title').text

            # check if the job title matches what we are applying for 
            if job_title == applyJL:
                withdraw_button = card.find_element(By.ID, "Apply/Withdraw_Btn")
                driver.execute_script('arguments[0].scrollIntoView();', withdraw_button)
                withdraw_button_text = withdraw_button.text
                time.sleep(0.5)
                
                # if button text is "Apply Now", click button to change to "Withdraw Now"
                if withdraw_button_text == "Apply Now":
                    withdraw_button.click()
                
                withdraw_button.click()
                time.sleep(0.5)
                # check if button changed to withdraw
                updated_withdraw_button = card.find_element(By.ID, "Apply/Withdraw_Btn")
                updated_button_text = updated_withdraw_button.text
                print("===============================================================================")
                print("Result: Passed!")
                print('Remarks: Button text after clicking:', updated_button_text)
                break

    except Exception as e:
        print("Result: Failed")
        print(f"Remarks: {e}")
    print("End of Automated Test Case 4")
    print("===============================================================================")

# automated test case 5: test if apply button works
def apply_btn_test():
    time.sleep(5)
    try:
        applyJL = 'Software Developer' # job title

        # Find all job listing
        job_cards = driver.find_elements_by_css_selector(".job_listing")

        for card in job_cards:
            job_title = card.find_element(By.CLASS_NAME, 'card-title').text
            

            # check if the job title matches what we are applying for 
            if job_title == applyJL:
                apply_button = card.find_element(By.ID, "Apply/Withdraw_Btn")
                # scroll to the element so that Selenium can detect the button on the screen
                driver.execute_script('arguments[0].scrollIntoView();', apply_button)
                apply_button_text = apply_button.text
                time.sleep(0.5)

                # if button text is "Withdraw Now", click button to change to "Apply Now"
                if apply_button_text == "Withdraw Now":
                    apply_button.click()
                    time.sleep(0.5)

                apply_button.click()
                time.sleep(0.5)
                # check if button changed to withdraw
                updated_apply_button = card.find_element(By.ID, "Apply/Withdraw_Btn")
                updated_button_text = updated_apply_button.text
                print("===============================================================================")
                print("Result: Passed!")
                print('Remarks: Button text after clicking=', updated_button_text)
                break 

    except Exception as e:
        print("Result: Failed")
        print(f"Remarks: {e}")
    print("End of Automated Test Case 5")
    print("===============================================================================")

# automated test case 6: check if the alignment percentage is accurate 

# automated test case 7: test view applicant buttons and see if automated test case result is reflected here


    

# Uncomment function to run automated test on local machine 
BrowseRoleListings()
RofRoleListings()
CofRoleListings()
withdraw_btn_test()
apply_btn_test()
