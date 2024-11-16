from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Chrome driver with Service
website = "https://www.linkedin.com/login"
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

# Wait until the search bar is available after login
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//input[contains(@class, "search-global-typeahead__input")]'))
)

# Locate the search bar input field directly and enter the search term
search_input = driver.find_element(By.XPATH, '//input[contains(@class, "search-global-typeahead__input")]')
search_input.click()
search_input.send_keys("Data Scientist")
time.sleep(2)  # Wait a short time before pressing Enter

search_input.send_keys(Keys.RETURN)
time.sleep(5)
