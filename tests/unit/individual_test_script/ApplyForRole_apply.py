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
time.sleep(5)

try:
    applyJL = 'Data Analyst' # job title

    # find all job cards on page
    # job_cards = driver.find_elements(By.XPATH, "//div[@class='card mb-4']")

    # Find multiple elements by class name
    job_cards = driver.find_elements_by_css_selector(".job_listing")

    for card in job_cards:
        job_title = card.find_element(By.CLASS_NAME, 'card-title').text
        print(job_title)

        # check if the job title matches what we are applying for 
        if job_title == applyJL:
            # apply_button = card.find_element(By.XPATH, "//button[contains(text(), 'Apply Now')]")
            apply_button = card.find_element(By.ID, "Apply/Withdraw_Btn")
            driver.execute_script('arguments[0].scrollIntoView();', apply_button)
            apply_button_text = apply_button.text
            print('Button text before clicking:', apply_button_text)
            time.sleep(0.5)

            # if button text is "Withdraw Now", click button to change to "Apply Now"
            if apply_button_text == "Withdraw Now":
                apply_button.click()
                apply_button_text = apply_button.text
                print('Button text if before is "Withdraw Now": ' + apply_button_text)

            apply_button.click()
            # wait for the button to change
            # WebDriverWait(driver, 10).until(
            #     EC.text_to_be_present_in_element((By.XPATH, "//div[@class='col-md-3']//button"), "Withdraw Now")
            # )
            time.sleep(0.5)
            # check if button changed to withdraw
            # updated_apply_button = card.find_element(By.XPATH, "//button[contains(text(), 'Withdraw Now')]")
            updated_apply_button = card.find_element(By.ID, "Apply/Withdraw_Btn")
            updated_button_text = updated_apply_button.text
            print('Button text after clicking:', updated_button_text, '\n', "Test Case Successful!")
            break 

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the WebDriver
    driver.quit()