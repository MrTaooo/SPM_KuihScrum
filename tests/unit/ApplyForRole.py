# import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# create webdriver object
driver = webdriver.Chrome()
# get url
driver.get("http://127.0.0.1:5500/templates/index.html")
# page loading
driver.implicitly_wait(10)

try:
    applyJL = 'Data Analyst' # job title

    # find all job cards on page
    job_cards = driver.find_elements(By.XPATH, "//div[@class='card mb-4']")

    for card in job_cards:
        job_title = card.find_element(By.CLASS_NAME, 'card-title').text
        print('job title', job_title)

        # check if the job title matches what we are applying for 
        if job_title == applyJL:
            apply_button = card.find_element(By.XPATH, "//button[contains(text(), 'Apply Now')]")
            apply_button_text = apply_button.text
            print('Button text before clicking:', apply_button_text)
            apply_button.click()
            # wait for the button text to change
            WebDriverWait(driver, 10).until(
                EC.text_to_be_present_in_element((By.XPATH, "//div[@class='col-md-3']//button"), "Withdraw")
            )
            # check if button changed to withdraw
            updated_apply_button = card.find_element(By.XPATH, "//button[contains(text(), 'Withdraw')]")
            updated_button_text = updated_apply_button.text
            print('Button text after clicking:', updated_button_text, '\n', "Test Case Successful!")
            
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the WebDriver
    driver.quit()

