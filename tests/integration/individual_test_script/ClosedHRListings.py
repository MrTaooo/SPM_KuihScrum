from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime

# create a webdriver object
driver = webdriver.Chrome()

# get url
driver.get("http://127.0.0.1:5500/templates/index.html")

try:
    # Ensure that 'hr' is clicked
    staff = driver.find_element(By.ID, "hr")
    staff.click()

    # find where listings are
    listings = driver.find_element(By.ID, "listing_list")

    # find all job listings
    job_listings = listings.find_elements(By.CLASS_NAME, "card.mb-4")

    count = 0
    actualClosed = 6

    today = datetime.now()

    for listing in job_listings:
        closing_date_element = listing.find_element(By.XPATH, ".//h5[contains(text(), 'Closing Date:')]")
        closing_date_text = closing_date_element.text.split(":")[1].strip()
        closing_date = datetime.strptime(closing_date_text, "%Y-%m-%d")
        formatted_closing_date = closing_date.strftime("%Y-%m-%d")
        if today > closing_date:
            count += 1
    
    if count == actualClosed:
        print("Test Case Passed: All closed listings are displayed.")

except NoSuchElementException as e:
    print("Test Case Failed")
    print(e)

finally:
    # Close the WebDriver
    driver.quit()
