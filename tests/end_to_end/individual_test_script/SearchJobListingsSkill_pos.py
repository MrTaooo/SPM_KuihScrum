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
# Scroll to the top of the page
driver.execute_script("window.scrollTo(0, 0);")
time.sleep(1)
# find all job listings 
try:
    # Find search by skill name 
    search_by_skill = driver.find_element(By.CLASS_NAME, "searchSkillName")
    time.sleep(1)
    search_by_skill.click() 
    time.sleep(1)

    # Find search bar 
    search_bar = driver.find_element(By.ID, "searchInput")
    search_bar.clear()
    time.sleep(1)
    skill_to_search = "Account Management"
    search_bar.send_keys(skill_to_search)
    time.sleep(1)
    # Find multiple elements by class name
    elements = driver.find_elements(By.CSS_SELECTOR,".job_listing")
    # Check each element's role name
    # Initialize a flag to check if the skill is present in entire skill section
    skill_found_in_all_listings = True

    for listing in elements:
        skills_section = listing.find_element(By.CLASS_NAME, "matchskills")
        time.sleep(1)
        skills = skills_section.find_elements(By.ID, "roleSkill")
        time.sleep(1)
        # Initialize a flag for the current listing
        skill_found_in_current_listing = False

        for skill in skills:
            skill_text = skill.text  # Extract the text of the "roleSkill" element
            print("SKILLTEXT:", skill_text)
            time.sleep(1)
            if skill_to_search == skill_text:
                skill_found_in_current_listing = True
                break

        if not skill_found_in_current_listing:
            skill_found_in_all_listings = False
            break
except NoSuchElementException:
    print("Test Case Failed")


# Check conditions
if skill_found_in_all_listings:
    print("Test case passed!")
else:
    print("Test case failed.")

print("End of Test Case")

