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
options.add_argument("--headless=new")
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
            time.sleep(1)
            job_title = listing.find_element(By.CLASS_NAME, 'card-title').text
            if job_list_name == job_title: 
                view_applicant_btn = listing.find_element(By.ID, "view_applicant_btn")
                driver.execute_script('arguments[0].scrollIntoView();', view_applicant_btn)
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

# automated test case 1: test if the staff can see only opened job listings (positive)
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

        # Assertion 
        assert number_of_elements == 2, "Number of elements is not equal to 1"

        # based on the test.sql, there should only be 2 job listings shown if a staff logs in
        if (number_of_elements == 2):
            print("Results: Passed!")
            print("Remarks: Job Listings Found and number of Job Listings matches expected number")
        else:
            print("Result: Failed.")
            print("Remarks: Number of listings displayed and should be seen do not match")
    except NoSuchElementException:
        print("Results: Failed")

    print("End of Automated Test Case 1")
    print("===============================================================================")

# automated test case 2: test if the hr can see all job listings (opened and closed) and can see the create and edit button on the UI (positive)
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

    # Assertion
    assert actual_create_name == expected_create_name, "Actual create name doesn't match the expected value"
    assert number_of_elements == 5, "Number of elements is not equal to 4"
    assert actual_edit_name == expected_edit_name, "Actual edit name doesn't match the expected value"

    # check conditions
    if (actual_create_name == expected_create_name) and (number_of_elements == 5) and (actual_edit_name == expected_edit_name):
        print("Result: Passed!")
        print("Remarks: HR can see buttons and open/close listings")
    else:
        print("Result: Failed.")
        print("Remarks: Number of listings displayed and should be seen do not match")

    print("End of Automated Test Case 2")
    print("===============================================================================")

# automated test case 3.1: test if the hr can create a new job listing (positive)
def test_CofRoleListings(roleTitle='IT Analyst', today=time.strftime("%Y-%m-%d"), new_closing_date="2023-12-25"):
    # Scroll to the top of the page
    driver.execute_script("window.scrollTo(0, 0);")
    hr = driver.find_element(By.ID, "hr")
    hr.click()
    time.sleep(1)

    # find create new role listing button and create a new role listing
    element = driver.find_element(By.ID, "create_listing_btn")
    element.click()
    time.sleep(5)
    dropdown = Select(driver.find_element(By.ID, "roleTitle")) 
    dropdown.select_by_visible_text(roleTitle)

    
    # Convert the input string to a datetime object
    input_date = datetime.strptime(new_closing_date, "%Y-%m-%d")
    # Format the datetime object as "%y-%m-%d"
    formatted_date_string = input_date.strftime("%m/%d/%Y")

    # Locate the date input field and enter the formatted date
    date_input = driver.find_element(By.ID, "closingDate")
    # Clear the existing value in the input field
    date_input.clear()  
    # Send the formatted date string
    date_input.send_keys(formatted_date_string)  
    time.sleep(1)

    # save job listing
    submit = driver.find_element(By.ID, "jobCreationButton")
    submit.click()
    time.sleep(1)

    # if we have alr ran the test script once, the next few codes will print out the message
    role_name, publish_date, closing_date = retrieve_Latest_Job_List()

    if role_name == roleTitle and publish_date == today and closing_date == new_closing_date:
        
        duplicate_create_err_msg = driver.find_element(By.ID, "errorMessage").text
        button_element = driver.find_element(By.ID, 'jobCreationCancelButton')
        button_element.click()
        time.sleep(5)
        return ["Duplicate", duplicate_create_err_msg]
        
    else: 
        # check if job listing alr created after running the test script once
        # first run of the day should be successful entry
        # subsequent runs of the day should be unsuccessful entry (duplicate entry)
        create_err_msg = driver.find_element(By.ID, "errorMessage").text
    
        if create_err_msg:
            create_modal = driver.find_element(By.ID, "createJob")
            close_button = create_modal.find_element(By.ID, "jobCreationCancelButton")
            close_button.click()
            time.sleep(1)
            if ("duplicate" in create_err_msg):
                return ["Overlap", create_err_msg]
            else: 
                return ["Invalid Closing Date", create_err_msg]
        else:
            # Wait for the top modal to be visible
            top_modal = driver.find_element(By.ID, "successModal")

            # Locate the close button within the top modal
            close_button = top_modal.find_element(By.ID, "closeModal")

            # Click the close button to close the top modal
            close_button.click()
            time.sleep(5)

            role_name, publish_date, closing_date = retrieve_Latest_Job_List()

            # Assertion 
            assert role_name == roleTitle, "Role name does not match role title"
            assert publish_date == today, "Publish date is not today's date"
            assert closing_date == new_closing_date, "Closing date does not match the expected formatted date string"
            assert not create_err_msg, "create_err_msg is not empty"

            # Check if first job list is the same as the one created (role name, publish date and closing date must match)
            print("===============================================================================")
            if role_name == roleTitle and publish_date == today and closing_date == new_closing_date:
                print("Result: Passed!")
                print("Remarks: Job listing created successfully")
            else:
                return "DB Connection Error"
            print("End of Automated test case 3.1")
            print("===============================================================================")

# automated test case 3.2: test if HR can create the exact same job listing with all the same details (negative)
def test_CofRoleListings_duplicate_exact():
    message = test_CofRoleListings()
    
    # Assertion
    assert message[0] == "Duplicate", "Duplicated entry created successfully"

    if (message[0] == "Duplicate"):
        print("===============================================================================")
        print("Result: Passed!")
        print("Remarks: Creation of duplicate job listing rejected")
        print(f"Error Message shown: {message[1]}")
        print("End of Automated test case 3.2")
        print("===============================================================================")

# automated test case 3.3: test if HR can create overlapping job listings for same role (negative)
# overlap closing date < open job listing closing date
def test_CofRoleListings_overlap():
    message = test_CofRoleListings(new_closing_date="2023-12-20")

    # Assertion
    assert message[0] == "Overlap", "Overlapping entry created successfully"

    if (message[0] =="Overlap"):
        print("===============================================================================")
        print("Result: Passed!")
        print("Remarks: Creation of overlapping job listing rejected")
        print("Parameters: Overlap closing date < open job listing closing date")
        print(f"Error Message shown: {message[1]}")
        print("End of Automated test case 3.3")
        print("===============================================================================")

# automated test case 3.4: test if HR can create overlapping job listings for same role (negative)
# overlap closing date > open job listing closing date
def test_CofRoleListings_overlap_2():
    message = test_CofRoleListings(new_closing_date="2024-01-01")

    # Assertion
    assert message[0] == "Overlap", "Overlapping entry created successfully"

    if (message[0] =="Overlap"):
        print("===============================================================================")
        print("Result: Passed!")
        print("Remarks: Creation of overlapping job listing rejected")
        print("Parameters: Overlap closing date > open job listing closing date")
        print(f"Error Message shown: {message[1]}")
        print("End of Automated test case 3.4")
        print("===============================================================================")

# automated test case 3.5: test if HR can create job listing where closing  date is before today (negative)
def test_CofRoleListings_invalid_publish_date():
    message = test_CofRoleListings(roleTitle="L&D Executive", new_closing_date="2023-09-10")

    # Assertion
    assert message[0] == "Invalid Closing Date", "Entry with invalid closing date created successfully"

    if (message[0] =="Invalid Closing Date"):
        print("===============================================================================")
        print("Result: Passed!")
        print("Remarks: Creation of job listing with invalid closing date rejected")
        print(f"Error Message shown: {message[1]}")
        print("End of Automated test case 3.5")
        print("===============================================================================")

# automated test case 4: test if withdraw button works [frontend test] (positive)
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

                # Assertion
                assert updated_button_text == "Apply Now", "Button text is not Apply Now"

                print("===============================================================================")
                print("Result: Passed!")
                print('Remarks: Button text after clicking:', updated_button_text)
                break

    except Exception as e:
        print("Result: Failed")
        print(f"Remarks: {e}")
    print("End of Automated Test Case 4")
    print("===============================================================================")

# automated test case 5: test view applicant buttons and see if withdraw button backend function works [backend] (postive)
def test_withdraw_backend():
    # Scroll to the top of the page
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    hr = driver.find_element(By.ID, "hr")
    hr.click()
    time.sleep(1)

    applicant_list = get_all_applicants_name()

    # Assertion
    assert "Derek Tan" not in applicant_list, "Derek Tan is in the applicant list"

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

# automated test case 6: test if apply button works [frontend] (positive)
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

                # Assertion
                assert updated_button_text == "Withdraw Now", "Button text is not Withdraw Now"

                print("===============================================================================")
                print("Result: Passed!")
                print('Remarks: Button text after clicking=', updated_button_text)
                break 

    except Exception as e:
        print("Result: Failed")
        print(f"Remarks: {e}")
    print("End of Automated Test Case 6")
    print("===============================================================================")

# automated test case 7: test view applicant buttons and see if apply button backend function works [backend] (positive)
def test_apply_backend():
    # Scroll to the top of the page
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    hr = driver.find_element(By.ID, "hr")
    hr.click()
    time.sleep(1)

    applicants = get_all_applicants_name()

    # Assertion
    assert "Derek Tan" in applicants, "Derek Tan is not in the applicant list"
    
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

# automated test case 8: check if the alignment percentage is accurate (positive)
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

                # Assertion
                assert calculated_percentage == progress_bar_text, "Calculated percentage does not match progress bar text"

                print("===============================================================================")
                if calculated_percentage == progress_bar_text:
                    print("Result: Passed!")
                    print(f"Remarks: Alignment Percentage for StaffID 140001 for Account Manager Role is {calculated_percentage}%")

    except Exception as e:
        print("Result: Failed")
        print(f"Remarks: {e.message}")
    print("End of Automated Test Case 8")
    print("===============================================================================")

# automated test case 9.1: test update of role listing closing date (positive)
def test_update_job_listing(job_list_index=0, input_closing_date="12/05/2023"):
    # Scroll to the top of the page
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    # ensure that 'hr' is clicked
    staff = driver.find_element(By.ID, "hr")
    staff.click()

    # Find all job listings
    try:
        # Find multiple elements by class name
        elements = driver.find_elements(By.CSS_SELECTOR, ".job_listing")
        joblist = elements[job_list_index]
        driver.execute_script('arguments[0].scrollIntoView();', joblist)
        time.sleep(1)
        
        # search for edit button
        edit = joblist.find_element(By.CLASS_NAME, "edit_btn")
        driver.execute_script('arguments[0].scrollIntoView();', edit)
        time.sleep(1)
        edit.click()
        time.sleep(1)
        date_input = driver.find_element(By.ID, "editClosingDate")

        # Clear the existing value in the input field
        date_input.clear()
        # Send the formatted date string
        date_input.send_keys(input_closing_date)
        time.sleep(1)

        # Click save to submit data to endpoint
        save_button = driver.find_element(By.ID, "editButton")
        save_button.click()
        time.sleep(1)

        error_message = driver.find_element(By.ID, "editErrorMessage").text
        
        if error_message:
            close_button = driver.find_element(By.ID, "editCancelButton")
            close_button.click()
            return error_message
        else:
            # Click close to close the modal
            close_button = driver.find_element(By.ID, "editCloseModal")
            close_button.click()
            time.sleep(1)
            driver.execute_script('arguments[0].scrollIntoView();', joblist)
            time.sleep(1)
            # Scroll up by 100 pixels
            driver.execute_script("window.scrollBy(0, -100);")
            time.sleep(1)
            closing_date = joblist.find_element(By.CLASS_NAME, "closingDate")
            closing_date_text = closing_date.text            
            # Convert the input date to a datetime object
            date_obj = datetime.strptime(input_closing_date, "%m/%d/%Y")
            # Format the date in YYYY-MM-DD format
            formatted_date = date_obj.strftime("%Y-%m-%d")
            # check conditions
            print("===============================================================================")
            if (closing_date_text == f"Closing Date: {formatted_date}"):
                print("Result: Passed!")
                print("Remarks: Job listing closing date updated successfully")
            else:
                print("Result: Failed")
                print("Remarks: Job listing closing date update failed. Closing date did not match input")

            print("End of Automated Test Case 9.1")
            print("===============================================================================")
    
    except NoSuchElementException:
            print("===============================================================================")
            print("Result: Failed")
            print("Remarks: Server error")
            print("End of Automated Test Case 9.1")
            print("===============================================================================")

# automated test case 9.2: test update of closed role listing (Account Manager) where closing date exceeds the current open role listing (Account Manager) (negative)
def test_update_job_listing_overlap():
    error_message = test_update_job_listing(job_list_index=-1)

    # Assertion
    assert "duplicate" in error_message, "Update of closed role listing accepted which results in duplicate listing"

    if ("duplicate" in error_message):
        print("===============================================================================")
        print("Result: Passed!")
        print("Remarks: Update of closed role listing rejected")
        print(f"Error Message shown: {error_message}")
        print("End of Automated Test Case 9.2")
        print("===============================================================================")

# automated test case 9.3: test update of role listing where input closing date is invalid (date before today) (negative)
def test_update_job_listing_invalid_closing_date():
    # Scroll to the top of the page
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    error_message = test_update_job_listing(job_list_index=0, input_closing_date="09/25/2023")

    # Assertion
    assert "before" in error_message, "Update of role listing with invalid closing date accepted"

    if ("before" in error_message):
        print("===============================================================================")
        print("Result: Passed!")
        print("Remarks: Update of role listing with invalid closing date rejected")
        print(f"Error Message shown: {error_message}")
        print("End of Automated Test Case 9.3")
        print("===============================================================================")

# automated test case 10.1: test search bar function (valid role name) (postive)
def test_search_function():
    # Scroll to the top of the page
    driver.execute_script("window.scrollTo(0, 0);")
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
        
        # Check conditions
        print("================================================================")
        if all_account_managers:

            assert all_account_managers , "Search function not working as expected"
            print("Result: Passed!")
            print("Remarks: Search Function working as expected")
        else:
            print("Result: Failed")
            print("Remarks: Search Function working not working")

        print("End of Automated Test Case 10.1")
        print("================================================================")
    except NoSuchElementException:
        print("===============================================================================")
        print("Result: Failed")
        print("Remarks: Selenium code error")
        print("End of Automated Test Case 10.1")
        print("===============================================================================")

# automated test case 10.2: test search bar function (invalid role name) (negative)
def test_invalid_search():
    # Scroll to the top of the page
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    # Find search bar 
    search_bar = driver.find_element(By.ID, "searchInput")
    search_bar.clear()
    search_bar.send_keys("zb")
    time.sleep(1)

    # Find multiple elements by class name
    elements = driver.find_elements(By.CSS_SELECTOR,".job_listing")

    assert len(elements) == 0, "Search function not working as expected"

    print("================================================================")
    if len(elements) > 0: 
        print("Result: Failed")
        print("Remarks: Search Function working not working") 
    else:    
        print("Result: Passed!")
        print("Remarks: Search function with invalid input works as expected")
    print("End of Automated Test Case 10.2")
    print("================================================================")
########################### End of Test Case Functions ######################################################

# Uncomment function to run automated test on local machine 
# Comment function when pushing to Git to ensure test functions are not run twice in GitHub actions
# Keyboard shortcuts --> Windows (Ctrl + /) Mac (Cmd + /) to comment and uncomment selected lines

test_BrowseRoleListings()
# test_RofRoleListings()
# test_CofRoleListings()
# test_CofRoleListings_duplicate_exact()
# test_CofRoleListings_overlap()
# test_CofRoleListings_overlap_2()
# test_CofRoleListings_invalid_publish_date()
# test_withdraw_btn_test()
# test_withdraw_backend()
# test_apply_btn_test()
# test_apply_backend()
# test_alignment_perc_accuracy()
# test_update_job_listing(0)
# test_update_job_listing_overlap()
# test_update_job_listing_invalid_closing_date()
# test_search_function()
# test_invalid_search()