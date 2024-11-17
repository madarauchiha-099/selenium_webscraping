import pandas as pd  # For saving data to CSV
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize the Chrome driver with Service
website = "https://www.linkedin.com/search/results/people/?keywords=university&origin=GLOBAL_SEARCH_HEADER&sid=XIV"
service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get(website)
driver.maximize_window()

# Log in to LinkedIn
username = driver.find_element(By.ID, 'username')
password = driver.find_element(By.ID, 'password')
username.send_keys('type your email')
password.send_keys('type your password')

login_button = driver.find_element(By.XPATH, '//button[@aria-label="Sign in"]')
login_button.click()

# Wait for the page to load completely
WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

# Storage for professor names
professor_name = []

# Set up the pagination limits
pages_to_scrape = 3
current_page = 1

while current_page <= pages_to_scrape:
    # Scroll down to ensure the page loads more results
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  #wait for the content to load

    # Locate the container and wait until it has loaded
    try:
        container = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "artdeco-card")]//ul[@role="list"]'))
        )
        
        # mark all professor entries
        products = container.find_elements(By.XPATH, './/li')
        
        # extract details for each entry
        for product in products:
            try:
                title = product.find_element(By.XPATH, './/span[@dir="ltr"][1]').text
                professor_name.append(title)
                print (title)
            except Exception as e:
                print(f"Error extracting product info: {e}")
                continue

        current_page += 1  # Move to the next page

        # Attempt to go to the next page
        try:
            # explicit wait for the next button to be clickable
            next_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Next"]'))
            )
            next_button.click()
            time.sleep(3)  # implicit wait
        except:
            print("No more pages left to scrape.")
            break

    except Exception as e:
        print(f"Error locating container or elements: {e}")
        break
        

# browser closed
driver.quit()

df_professors = pd.DataFrame({'Professor Name': professor_name})

#save to CSV
df_professors.to_csv('professor_names.csv', index=False)
#save to json
df_professor.to_json("professor_names.json")
