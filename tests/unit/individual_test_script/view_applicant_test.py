# import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# create webdriver object
# Define ChromeOptions to run headless
chrome_options = webdriver.ChromeOptions()
# headless means that the browser will not open up
# chrome_options.add_argument("--headless")

# Use ChromeDriverManager to download and manage ChromeDriver
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# get url
driver.get("http://127.0.0.1:5500/templates/index.html")
driver.maximize_window()
hr = driver.find_element(By.ID, "hr")
hr.click()
time.sleep(1)

try: 
    # comparison data for staff with ID 1 who applied for Data Analyst job listing in automated test case 5 

    job_list_name = 'Marketing Specialist'

    job_listings = driver.find_elements_by_css_selector(".job_listing")
    for listing in job_listings:
        job_title = listing.find_element(By.CLASS_NAME, 'card-title').text
        if job_list_name == job_title: 
            view_applicant_btn = listing.find_element(By.ID, "view_applicant_btn")
            
            # scroll to see the button on the screen
            driver.execute_script('arguments[0].scrollIntoView();', view_applicant_btn)
            # Scroll down by a specified number of pixels (e.g., 500 pixels)
            scroll_distance = 800
            driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
            time.sleep(2)

            view_applicant_btn.click()
            time.sleep(1)
            
            # Find the parent element whose child elements you want to count
            parent_element = driver.find_element_by_id("applicant_table")  
            # Find the child elements using a locator strategy (e.g., find all child div elements)
            child_elements = parent_element.find_elements_by_tag_name("tr")
            # Get the count of child elements
            number_of_children = len(child_elements)

            applicant_list = []
            if number_of_children > 0:
            # Get the text content of the first child element (first <tr>)
                for child in child_elements:
                    applicant_name = child.find_element(By.ID, "applicant_name")
                    applicant_list.append(applicant_name.text)
            

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()