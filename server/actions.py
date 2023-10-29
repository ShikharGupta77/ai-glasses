from seleniumbase import SB
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# date is YYYY/MM/DD
def calendar_add(date, startTime, endTime, title):
    with SB(uc=True, headed=True) as driver:
        
        driver.get("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fwww.google.com%2F&ec=GAZAmgQ&hl=en&ifkv=AVQVeyynx9vTWrORetNTDJstyP9KRREywFTztGbPzXPZOA0CLrrBLZexaIuorYLmTqCW3xH2qcyPmg&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-653967197%3A1698546704446367&theme=glif")
        driver.type("#identifierId", 'calhacks224')
        driver.click("#identifierNext > div > button")
        driver.type("#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input", 'Dortnite@1233')
        driver.click("#passwordNext > div > button")
        time.sleep(3)
        driver.get(f'https://calendar.google.com/calendar/u/0/r/day/{date}')
        element = driver.find_element(By.CSS_SELECTOR, ".WJVfWe.A3o4Oe")
        element.click()
        
        startTimeElement = driver.find_element(By.XPATH, '//*[@data-key="startTime"]')
        endTimeElement = driver.find_element(By.XPATH, '//*[@data-key="endTime"]')
        time.sleep(5)
        driver.execute_script("arguments[0].textContent = arguments[1];", startTimeElement, startTime)
        driver.execute_script("arguments[0].textContent = arguments[1];", endTimeElement, endTime)
        
        input_element = driver.find_element(By.CSS_SELECTOR, ".VfPpkd-fmcmS-wGMbrd")
        #titleElement.click()
        #time.sleep(2)
        #driver.execute_script("arguments[0].setAttribute('value', arguments[1]);", titleElement, title)
        #driver.execute_script("arguments[0].textContent = arguments[1];", titleElement, "Your New Text")
        #input_element = driver.find_element(By.CSS_SELECTOR, '#c4305')
        #driver.execute_script("arguments[0].setAttribute('placeholder', 'New Placeholder')", input_element)
        #driver.execute_script("arguments[0].setAttribute('aria-label', 'New Aria Label')", input_element)
        # Assuming you've found the input_element as shown above
        #input_element.clear()  # Clear existing value/text
        #input_element.send_keys('New Text')  # This simulates typing into the input field
        time.sleep(2)
        saveButton = driver.find_element(By.CSS_SELECTOR, ".VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-k8QpJ.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.nCP5yc.AjY5Oe.DuMIQc.LQeN7.pEVtpe")
        saveButton.click()
        time.sleep(15)

def slack_add(message):
    with SB(uc=True, headed=True) as driver:
        driver.get("https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fwww.google.com%2F&ec=GAZAmgQ&hl=en&ifkv=AVQVeyynx9vTWrORetNTDJstyP9KRREywFTztGbPzXPZOA0CLrrBLZexaIuorYLmTqCW3xH2qcyPmg&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-653967197%3A1698546704446367&theme=glif")
        driver.type("#identifierId", 'calhacks224')
        driver.click("#identifierNext > div > button")
        driver.type("#password > div.aCsJod.oJeWuf > div > div.Xb9hP > input", 'Dortnite@1233')
        driver.click("#passwordNext > div > button")
        time.sleep(2)
        driver.get("https://slack.com/signin#/signin")
        googleButton = driver.find_element(By.CSS_SELECTOR, "#google_login_button")
        googleButton.click()
        signInButton = driver.find_element(By.CSS_SELECTOR, ".lCoei.YZVTmd.SmR8")
        signInButton.click()
        print(signInButton)
        

       
if __name__ == '__main__':
    #calendar_add(date='2023/10/29', startTime='7:00pm', endTime='8:00pm', title="Meeting with Kushi")
    slack_add("Hello there!")