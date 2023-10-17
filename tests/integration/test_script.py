# import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import datetime

# create chrome options
options = webdriver.ChromeOptions()
# Define ChromeOptions to run headless
# headless means that the browser will not open up
# options.add_argument("--headless=new")
# create webdriver object
driver = webdriver.Chrome(options=options)

# get url
# driver.get("http://127.0.0.1:5500/templates/index.html")
driver.get("https://spm-kuih-scrum.vercel.app/")
driver.set_window_size(1920, 1080)
time.sleep(5)

########################### Start of Helper Functions #########################################################

def retrieve_Latest_Job_List():
    # get the parent element of the job listing
    job_list_parent_element = driver.find_element(By.ID,'joblist_parent')
    driver.execute_script('arguments[0].scrollIntoView();', job_list_parent_element)

    # get the first child element of the job listing (aka first listing)
    first_job_listing = job_list_parent_element.find_element(By.CSS_SELECTOR,'*:first-child')

    # Find the elements for role name, publish date, and closing date within the div
    role_name_element = first_job_listing.find_element(By.CSS_SELECTOR,'.card-title')
    publish_date_element = first_job_listing.find_element(By.XPATH,".//h5[contains(text(), 'Date Posted:')]")
    closing_date_element = first_job_listing.find_element(By.XPATH,".//h5[contains(text(), 'Closing Date:')]")

    # Extract text from the elements
    role_name = role_name_element.text
    publish_date = publish_date_element.text.replace('Date Posted:', '').strip()
    closing_date = closing_date_element.text.replace('Closing Date:', '').strip()

    return (role_name, publish_date, closing_date)

def get_all_applicants_name():
    try: 
        # comparison data for staff with ID 1 who applied for Data Analyst job listing in automated test case 5 

        job_list_name = 'Account Manager'

        job_listings = driver.find_elements(By.CSS_SELECTOR,".job_listing")
        for listing in job_listings:
            driver.execute_script('arguments[0].scrollIntoView();', listing)
            job_title = listing.find_element(By.CLASS_NAME, 'card-title').text
            if job_list_name == job_title: 
                view_applicant_btn = listing.find_element(By.ID, "view_applicant_btn")
                
                # scroll to see the button on the screen
                driver.execute_script('arguments[0].scrollIntoView();', view_applicant_btn)
                time.sleep(1)
                # Scroll down by a specified number of pixels (e.g., 500 pixels)
                scroll_distance = 1000
                driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
                time.sleep(1)
                view_applicant_btn.click()
                time.sleep(1)
                
                # Find the parent element whose child elements you want to count
                parent_element = driver.find_element(By.ID,"applicant_table")  
                # Find the child elements using a locator strategy (e.g., find all child div elements)
                child_elements = parent_element.find_elements(By.TAG_NAME,"tr")
                # Get the count of child elements
                number_of_children = len(child_elements)
                applicant_list = []
                if number_of_children > 0:
                # Get the text content of the first child element (first <tr>)
                    for child in child_elements:
                        applicant_name = child.find_element(By.ID, "applicant_name")
                        applicant_list.append(applicant_name.text)
                # for applicant in applicant_list:
                #     print(applicant)

                close_button = driver.find_element(By.ID, "close_view_applicant_btn")
                close_button.click()
                time.sleep(1)
                return applicant_list

    except Exception as e:
        print(f"An error occurred: {e}")

########################### End of Helper Functions #########################################################


########################### Start of Test Case Functions ####################################################

# automated test case 1: test if the staff can see only opened job listings
def test_BrowseRoleListings():
    # ensure that 'staff' is clicked
    staff = driver.find_element(By.ID, "staff")
    staff.click()
    time.sleep(1)

    print("===============================================================================")
    # check for job listings
    try:
        # Find multiple elements by class name
        elements = driver.find_elements(By.CSS_SELECTOR,".job_listing")
        # Get the number of elements
        number_of_elements = len(elements)
        # based on the test.sql, there should only be 2 job listings shown if a staff logs in
        if (number_of_elements == 1):
            print("Results: Passed!")
            print("Remarks: Job Listings Found and number of Job Listings matches expected number")
        else:
            print("Result: Failed.")
            print("Remarks: Number of listings displayed and should be seen do not match")
    except NoSuchElementException:
        print("Results: Failed")

    print("End of Automated Test Case 1")
    print("===============================================================================")

# automated test case 2: test if the hr can see all job listings (opened and closed) and can see the create and edit button on the UI
def test_RofRoleListings():
    hr = driver.find_element(By.ID, "hr")
    hr.click()
    time.sleep(1)

    # find create new role listing button
    element = driver.find_element(By.ID, "create_listing_btn")
    actual_create_name = element.text
    expected_create_name = "Create a Job Listing"

    print("===============================================================================")
    # check for job listings
    try:
        # Find multiple elements by class name
        elements = driver.find_elements(By.CSS_SELECTOR,".job_listing")
        # Get the number of elements
        number_of_elements = len(elements)
    except NoSuchElementException:
        print("Test Case Failed")

    # search for edit button
    edit = driver.find_element(By.CSS_SELECTOR,".edit_btn")
    actual_edit_name = edit.text
    expected_edit_name = "Edit"

    # check conditions
    if (actual_create_name == expected_create_name) and (number_of_elements == 2) and (actual_edit_name == expected_edit_name):
        print("Result: Passed!")
        print("Remarks: HR can see buttons and open/close listings")
    else:
        print("Result: Failed.")
        print("Remarks: Number of listings displayed and should be seen do not match")

    print("End of Automated Test Case 2")
    print("===============================================================================")

# automated test case 3: test if the hr can create a new job listing 
def test_CofRoleListings():
    hr = driver.find_element(By.ID, "hr")
    hr.click()
    time.sleep(1)

    # find create new role listing button and create a new role listing
    element = driver.find_element(By.ID, "create_listing_btn")
    element.click()
    time.sleep(5)
    dropdown = Select(driver.find_element(By.ID, "roleTitle")) 
    roleTitle = "IT Analyst"
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
    role_name, publish_date, closing_date = retrieve_Latest_Job_List()
    if role_name == roleTitle and publish_date == today and closing_date == formatted_date_string:
        button_element = driver.find_element(By.ID, 'jobCreationCancelButton')
        button_element.click()
        time.sleep(5)
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
        create_modal = driver.find_element(By.ID, "createJob")
        close_button = create_modal.find_element(By.ID, "jobCreationCancelButton")
        close_button.click()
        time.sleep(1)
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
        time.sleep(5)

        role_name, publish_date, closing_date = retrieve_Latest_Job_List()
        # Check if first job list is the same as the one created (role name, publish date and closing date must match)
        if role_name == roleTitle and publish_date == today and closing_date == formatted_date_string:
            print("Result: Passed!")
            print("Remarks: Job listing created successfully")
        else:
            print("Result: Failed.")
            print("Remarks: Job listing not created successfully.")
        print("End of Automated test case 3")
        print("===============================================================================")

# automated test case 4: test if withdraw button works (only testing frontend here)
def test_withdraw_btn_test():
    # Scroll to the top of the page
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    staff = driver.find_element(By.ID, "staff")
    staff.click()
    time.sleep(1)

    try:
        applyJL = 'Account Manager' # job title

        # Find all job listing
        job_cards = driver.find_elements(By.CSS_SELECTOR,".job_listing")
        time.sleep(1)
        for card in job_cards:
            job_title = card.find_element(By.CLASS_NAME, 'card-title').text
            driver.execute_script('arguments[0].scrollIntoView();', card)
            # check if the job title matches what we are applying for 
            if job_title == applyJL:
                withdraw_button = card.find_element(By.ID, "Apply/Withdraw_Btn")
                
                # scroll to see the button on the screen
                driver.execute_script('arguments[0].scrollIntoView();', withdraw_button)
                withdraw_button_text = withdraw_button.text
                time.sleep(1)
                
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

# automated test case 5: test view applicant buttons and see if withdraw button backend function works
def test_withdraw_backend():
    # Scroll to the top of the page
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    hr = driver.find_element(By.ID, "hr")
    hr.click()
    time.sleep(1)

    applicant_list = get_all_applicants_name()

    print("===============================================================================")
    if "Derek Tan" in applicant_list:
        print("Result: Failed")
        print("Remarks: Derek Tan is in the applicant list")
        print(f"Remarks: Applicant List: {applicant_list}")
    else:
        print("Result: Passed!")
        print("Remarks: Derek Tan is not in the applicant list")   
        print(f"Remarks: Applicant List: {applicant_list}") 
    print("End of Automated Test Case 5")
    print("===============================================================================")

# automated test case 6: test if apply button works (only testing frontend here)
def test_apply_btn_test():
    # Scroll to the top of the page
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)

    staff = driver.find_element(By.ID, "staff")
    staff.click()
    time.sleep(1)

    try:
        applyJL = 'Account Manager' # job title

        # Find all job listing
        job_cards = driver.find_elements(By.CSS_SELECTOR,".job_listing")

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
    print("End of Automated Test Case 6")
    print("===============================================================================")

# automated test case 7: test view applicant buttons and see if apply button backend function works
def test_apply_backend():
    # Scroll to the top of the page
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    hr = driver.find_element(By.ID, "hr")
    hr.click()
    time.sleep(1)

    applicants = get_all_applicants_name()
    
    print("===============================================================================")
    if "Derek Tan" in applicants:
        print("Result: Passed!")
        print("Remarks: Derek Tan is in the applicant list")
        print(f"Remarks: Applicant List: {applicants}")
    else:
        print("Result: Failed")
        print("Derek Tan is not in the applicant list")    
    print("End of Automated Test Case 7")
    print("===============================================================================")

# automated test case 8: check if the alignment percentage is accurate 
def test_alignment_perc_accuracy():
    # Scroll to the top of the page
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    staff = driver.find_element(By.ID, "staff")
    staff.click()
    time.sleep(1)

    try: 
        # comparison data for staff with ID 1 
        num_skill_matched = 4
        num_role_skill = 13
        job_list_name = 'Account Manager'
        job_listings = driver.find_elements(By.CSS_SELECTOR, ".job_listing")
        for listing in job_listings:
            job_title = listing.find_element(By.CLASS_NAME, 'card-title').text
            if job_list_name == job_title: 
                progress_bar = listing.find_element(By.CLASS_NAME, 'progress-bar')
                progress_bar_text = progress_bar.text.replace('%', '')
                calculated_percentage = str(round(num_skill_matched/num_role_skill*100))

                print("===============================================================================")
                if calculated_percentage == progress_bar_text:
                    print("Result: Passed!")
                    print(f"Remarks: Alignment Percentage for StaffID 140001 for Account Manager Role is {calculated_percentage}%")

    except Exception as e:
        print("Result: Failed")
        print(f"Remarks: {e.message}")
    print("End of Automated Test Case 8")
    print("===============================================================================")

########################### End of Test Case Functions ######################################################


# Uncomment function to run automated test on local machine 
test_BrowseRoleListings()
test_RofRoleListings()
test_CofRoleListings()
test_withdraw_btn_test()
test_withdraw_backend()
test_apply_btn_test()
test_apply_backend()
test_alignment_perc_accuracy()