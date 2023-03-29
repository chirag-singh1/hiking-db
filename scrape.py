from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.by import By
from selenium import webdriver

import traceback

# Initialize web driver
service = Service(executable_path="/home/chirag/Downloads/chromedriver_linux64/chromedriver")
options = Options()
options.add_argument("--headless=new")
driver = webdriver.Chrome(service=service, options=options)

# Get first page, wait for it to load
driver.get("https://www.hikingproject.com/directory/8007121/california")
wait = WebDriverWait(driver, timeout=10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException])
try:
    while True:
        show_more_button = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "load-more-trails"))
        )
        show_more_button.click()

except Exception as e:
    print('Iterations', i)
    traceback.print_exception()
    trail_arr = driver.find_elements(By.CLASS_NAME, value='trail-row')
    for t in trail_arr:
        print(t.get_attribute('data-href'))

driver.quit()
