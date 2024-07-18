import time
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wait_for_element(driver, xpath, indefinetly=True, interval=1):
    if indefinetly:
        while True:
            try:
                element = WebDriverWait(driver, interval).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                return element
            except TimeoutException:
                pass
    else:
        try:
            element = WebDriverWait(driver, interval).until(EC.visibility_of_element_located((By.XPATH, xpath)))
            return element
        except TimeoutException:
            return None

#remove this later
def click_with_retry(driver, xpath, retries=5):
    for _ in range(retries):
        try:
            element = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, xpath)
                )
            )
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            return
        except ElementClickInterceptedException:
            time.sleep(1)
    raise Exception(f"Could not click element with xpath: {xpath}")
# def checkElementVisibility(driver, xpath):
#     try:
#         WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, xpath)))
#         return True
#     except TimeoutException:
#         return False
    
def waitForPage(driver):
    print("Waiting for page to load...")
    
    loaded = WebDriverWait(driver, 25).until(
        lambda d: d.execute_script("return document.readyState") == "complete" or "interactive"
    )   
    
    if not loaded:
        print("Page not loaded...")
        return False
    else:
        print("Page loaded...")
        return True
