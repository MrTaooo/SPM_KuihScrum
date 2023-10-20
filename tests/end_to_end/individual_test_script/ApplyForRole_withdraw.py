# import webdriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import time

chrome_options = webdriver.ChromeOptions()
# headless means that the browser will not open up
# chrome_options.add_argument("--headless")

# Use ChromeDriverManager to download and manage ChromeDriver
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# get url
driver.get("http://127.0.0.1:5500/templates/index.html")

try:
    time.sleep(5)
    applyJL = 'Software Developer' # job title

    # find all job cards on page
    # job_cards = driver.find_elements(By.XPATH, "//div[@class='card mb-4']")
    # Find all job listing
    job_cards = driver.find_elements_by_css_selector(".job_listing")

    for card in job_cards:
        job_title = card.find_element(By.CLASS_NAME, 'card-title').text
        print('job title', job_title)

        # check if the job title matches what we are applying for 
        if job_title == applyJL:
            # apply_button = card.find_element(By.XPATH, "//button[contains(text(), 'Withdraw')]")
            # apply_button_text = apply_button.text
            withdraw_button = card.find_element(By.ID, "Apply/Withdraw_Btn")
            driver.execute_script('arguments[0].scrollIntoView();', withdraw_button)
            withdraw_button_text = withdraw_button.text
            time.sleep(0.5)
            print('Button text before clicking:', withdraw_button_text)
            
            # if button text is "Apply Now", click button to change to "Withdraw Now"
            if withdraw_button_text == "Apply Now":
                withdraw_button.click()
            
            withdraw_button.click()
            time.sleep(0.5)
            # wait for the button text to change
            # WebDriverWait(driver, 10).until(
            #    EC.text_to_be_present_in_element((By.XPATH, "//div[@class='col-md-3']//button"), "Apply Now")
            # )
            # check if button changed to withdraw
            # updated_withdraw_button = card.find_element(By.XPATH, "//button[contains(text(), 'Apply Now')]")
            updated_withdraw_button = card.find_element(By.ID, "Apply/Withdraw_Btn")
            updated_button_text = updated_withdraw_button.text
            print('Button text after clicking:', updated_button_text, '\n', "Test Case Successful!")
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the WebDriver
    driver.quit()